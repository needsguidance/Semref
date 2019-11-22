import ntpath
import os
import time
from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.metrics import MetricsBase, dp, sp
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivymd.theming import ThemeManager
from kivymd.toast import toast
from kivymd.uix.button import MDFillRoundFlatIconButton, MDIconButton
from kivymd.uix.dialog import MDDialog, MDInputDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationdrawer import (MDNavigationDrawer, MDToolbar,
                                         NavigationDrawerIconButton,
                                         NavigationDrawerSubheader,
                                         NavigationLayout)

from GUI.IO.devices import (ASCIIGrid, HexKeyboard, SevenSegmentDisplay,
                            TrafficLights)
from assembler import (Assembler, clear_ram, hexify_ram_content,
                       verify_ram_content)
from assembler import RAM as RAM_ASSEMBLER
from lexer import SemrefLexer
from microprocessor_simulator import RAM, MicroSim
from utils import (ASCII_TABLE, EVENTS, HEX_KEYBOARD, REGISTER,
                   SEVEN_SEGMENT_DISPLAY, TRAFFIC_LIGHT, is_valid_port,
                   update_indicators, update_reserved_ports, hex_to_binary)


class DataWindow(FloatLayout):
    """
    Collection of widgets that displays data.
    User will see the following:
        - Register Table
        - Memory Table
        - 7 Segment Display
        - LED lights organized as traffic lights
        - ASCII Grid
    """

    def __init__(self, **kwargs):
        self.app = kwargs.pop('app')
        self.micro_sim = kwargs.pop('micro_sim')
        self.dpi = kwargs.pop('dpi')
        super(DataWindow, self).__init__(**kwargs)
        self.ascii = ASCIIGrid(dpi=self.dpi)
        self.reg_table = RegisterTable(dpi=self.dpi)
        self.mem_table = MemoryTable(dpi=self.dpi)
        self.inst_table = InstructionTable(dpi=self.dpi)
        self.light = TrafficLights()
        self.editor = TextEditor(dpi=self.dpi)
        self.seven_segment_display = SevenSegmentDisplay()
        self.hex_keyboard_label = Label(text='HEX KEYBOARD',
                                        font_size=sp(20),
                                        color=(0, 0, 0, 1))

        # Create variable of scheduling instance so that it can be turned on and off,
        # to avoid repeat of the same thread

        self.editor_loader = Clock.schedule_interval(self.check_loader, 0.1)

        self.blinking_on = Clock.schedule_interval(self.light.intermittent_on,
                                                   0.5)
        self.blinking_off = Clock.schedule_interval(self.light.intermittent_off,
                                                    0.3)

        self.event_io = Clock.create_trigger(self.update_io)
        self.event_data_tables = Clock.create_trigger(self.update_data_tables)
        self.inst_table.get_data(self.micro_sim.index,
                                 self.micro_sim.disassembled_instruction())
        self.event_data_tables()

        # Since the instancing of the events actually starts the scheduling, needs to be canceled right away
        self.blinking_on.cancel()
        self.blinking_off.cancel()

        self.hex_keyboard_layout = HexKeyboard(mem_table=self.mem_table,
                                               dpi=self.dpi)
        box = FloatLayout()
        box.add_widget(self.hex_keyboard_layout)
        box.add_widget(self.hex_keyboard_label)
        self.popup = Popup(title='Hex Keyboard',
                           content=box,
                           background='assets/images/plain-white-background.jpg',
                           title_color=(0, 0, 0, 0),
                           separator_color=(1, 1, 1, 1))
        if self.dpi < 192:
            self.popup.size_hint = (None, None)
            self.popup.size = (450, 400)

            self.hex_keyboard_label.pos_hint = {
                'x': dp(0.01),
                'y': dp(0.35)
            }
        else:
            self.popup.size_hint_x = dp(0.3)
            self.popup.size_hint_y = dp(0.3)
            self.popup.pos_hint = {
                'x': dp(0.1),
                'y': dp(0.13)
            }

            self.hex_keyboard_label.pos_hint = {
                'x': dp(0.01),
                'y': dp(0.13)
            }
        self.add_widget(self.reg_table)
        self.add_widget(self.inst_table)
        self.add_widget(self.mem_table)
        self.add_widget(self.light)
        self.add_widget(self.seven_segment_display)
        self.add_widget(self.editor)
        self.add_widget(self.ascii)

    def check_loader(self, dt):
        """
        Checks if a file is loaded
        :param dt: float
        """
        if EVENTS['FILE_PATH'] and EVENTS['CAN_WRITE']:
            self.editor.load_file(EVENTS['FILE_PATH'])
            EVENTS['CAN_WRITE'] = False

    def open_keyboard(self, instance):
        """
        Opens dialog box with hex keyboard
        :param instance: obj
        """
        self.popup.open()

    def update_io(self, dt):
        """
        Updates IO devices on run/debug events
        :param dt: float
        """
        self.light.change_color(hex_to_binary(f'{RAM[TRAFFIC_LIGHT["port"]]}'))
        self.seven_segment_display.activate_segments(
            hex_to_binary(f'{RAM[SEVEN_SEGMENT_DISPLAY["port"]]}'))
        self.ascii.update_ascii_grid()

    def update_data_tables(self, dt):
        """
        Updates Register, and Memory tables
        :param dt: float
        """
        self.reg_table.get_data()
        self.mem_table.data_list.clear()
        self.mem_table.get_data()


class MainWindow(BoxLayout):
    """Contains navbar buttons and DataWindow to display UI"""

    def __init__(self, **kwargs):
        self.nav_drawer = kwargs.pop('nav_drawer')
        self.app = kwargs.pop('app')
        self.micro_sim = kwargs.pop('micro_sim')
        self.dpi = kwargs.pop('dpi')
        super().__init__(**kwargs)
        self.buttons_y_pos = dp(0.2) if self.dpi < 192 else dp(0.1)

        self.first_inst = True
        self.step_index = 0
        self.ids['left_actions'] = BoxLayout()
        self.orientation = 'vertical'
        self.toolbar_layout = BoxLayout(orientation='vertical')
        self.menu_items = [
            {
                'viewclass': 'MDMenuItem',
                'text': 'Save Register/Memory Content',
                'callback': self.open_reg_mem_save_dialog,
            },
            {
                'viewclass': 'MDMenuItem',
                'text': 'Save Editor Content',
                'callback': self.open_editor_save_dialog
            }
        ]
        self.run_window = DataWindow(app=self.app,
                                     micro_sim=self.micro_sim,
                                     dpi=self.dpi)
        self.md_toolbar = MDToolbar(title='Semref Micro Sim',
                                    md_bg_color=self.app.theme_cls.primary_color,
                                    background_palette='Primary',
                                    background_hue='500',
                                    elevation=10,
                                    ids=self.ids,
                                    left_action_items=[
                                        [
                                            'dots-vertical',
                                            lambda x: self.nav_drawer.toggle_nav_drawer()
                                        ]
                                    ])
        self.run_button = MDFillRoundFlatIconButton(text='Run',
                                                    icon='run',
                                                    size_hint=(None, None),
                                                    pos_hint={
                                                        'y': self.buttons_y_pos
                                                    },
                                                    on_release=self.execute_micro_instructions)
        self.debug_button = MDFillRoundFlatIconButton(text='Debug',
                                                      icon='android-debug-bridge',
                                                      size_hint=(None, None),
                                                      pos_hint={
                                                          'y': self.buttons_y_pos
                                                      },
                                                      on_release=lambda *args: self.execute_micro_instructions(*args, mode='debug'))
        self.refresh_button = MDFillRoundFlatIconButton(text='Clear',
                                                        icon='refresh',
                                                        size_hint=(None, None),
                                                        pos_hint={
                                                            'y': self.buttons_y_pos
                                                        },
                                                        on_release=self.clear_dialog)
        self.save_button = MDFillRoundFlatIconButton(text='Save File',
                                                     icon='download',
                                                     size_hint=(None, None),
                                                     pos_hint={
                                                         'y': self.buttons_y_pos
                                                     },
                                                     on_release=lambda x: MDDropdownMenu(items=self.menu_items,
                                                                                         width_mult=4).open(
                                                         self.save_button))
        self.pop_button = MDFillRoundFlatIconButton(text='Hex Keyboard',
                                                    icon='keyboard-outline',
                                                    size_hint=(None, None),
                                                    pos_hint={
                                                        'y': self.buttons_y_pos
                                                    },
                                                    on_release=self.run_window.open_keyboard)
        self.loaded_file = MDIconButton(icon='file-check',
                                        size_hint=(None, None),
                                        pos_hint={
                                            'y': self.buttons_y_pos
                                        }, theme_text_color='Custom',
                                        text_color=[0, 0.6, 0, 1],
                                        on_release=self.buttons_information
                                        )
        self.not_loaded_file = MDIconButton(icon='file-alert',
                                            size_hint=(None, None),
                                            pos_hint={
                                                'y': self.buttons_y_pos
                                            }, theme_text_color='Custom',
                                            text_color=self.app.theme_cls.accent_dark,
                                            on_release=self.buttons_information
                                            )
        self.md_toolbar.add_widget(self.run_button)
        self.md_toolbar.add_widget(self.debug_button)
        self.md_toolbar.add_widget(self.refresh_button)
        self.md_toolbar.add_widget(self.save_button)
        self.md_toolbar.add_widget(self.pop_button)
        self.add_widget(self.md_toolbar)
        self.add_widget(self.run_window)
        self.add_widget(self.not_loaded_file)

    def execute_micro_instructions(self, instance, mode='run'):
        """
        Runs micro instructions in the specified mode
            run -> from start to finish
            debug -> step-by-step execution
        :param instance: obj
        :param mode: str
        """
        toast_message = 'File executed successfully'
        if not self.run_window.editor.valid_text and not EVENTS['IS_OBJ']:
            toast("Invalid code. Load file to run or write valid code in editor")
        elif EVENTS['EDITOR_SAVED']:
            if mode == 'run':
                self.clear_run()

            # If file is an .obj file, runs simulator
            if EVENTS['FILE_PATH'].endswith('.obj'):
                self.load_micro_sim_ram(EVENTS['FILE_PATH'])
            else:
                self.assembler()

            if mode == 'run':
                self.run_micro_instructions(toast_message)
            else:
                self.debug_micro_instructions(toast_message)
        else:
            toast('Please save changes on editor before running')

    def run_micro_instructions(self, toast_message):
        """
        Runs micro instructions from start to finish
        :param toast_message: str
        """
        self.micro_sim.is_running = True
        if self.micro_sim.is_ram_loaded:
            self.run_window.inst_table.get_data(self.micro_sim.index,
                                                self.micro_sim.disassembled_instruction())

            self.run_window.blinking_on()
            self.run_window.blinking_off()

            timeout = time.time() + 5  # 5 seconds from now
            while self.micro_sim.is_running:
                try:
                    self.micro_sim.run_micro_instructions(timeout)
                    self.run_window.inst_table.get_data(self.micro_sim.index,
                                                        self.micro_sim.disassembled_instruction())
                except (SystemError, TimeoutError) as e:
                    toast_message = f'Error! {e}'
            self.first_inst = False
            self.run_window.event_data_tables()
            self.run_window.event_io()
            toast(toast_message)

    def debug_micro_instructions(self, toast_message):
        """
        Step-by-step execution of microprocessor instructions
        :param toast_message: str
        """
        if self.micro_sim.is_ram_loaded:
            self.step_index += 1
        if self.first_inst:
            self.micro_sim.is_running = True
            self.run_window.inst_table.get_data(self.micro_sim.index,
                                                self.micro_sim.disassembled_instruction())
            self.first_inst = False
        elif self.micro_sim.is_running:
            self.micro_sim.run_micro_instructions()
            self.run_window.inst_table.get_data(self.micro_sim.index,
                                                self.micro_sim.disassembled_instruction())
            toast(
                f'Running instruction in step-by-step mode. Step {self.step_index} is running')
            self.run_window.event_data_tables()
            self.run_window.event_io()
        else:
            toast('File executed successfully')

    def assembler(self):
        """
        Assembles source code and generate obj file
        """
        i = 0
        # Obtains last name on path string using ntpath and then
        # strips file extension using os.path.splitext
        # Should work across different OS
        filename = os.path.splitext(ntpath.basename(EVENTS['FILE_PATH']))[0]
        try:
            asm = Assembler(filename=EVENTS['FILE_PATH'])
            asm.read_source()
            asm.store_instructions_in_ram()
            verify_ram_content()
            hexify_ram_content()
            output_file_location = f'output/{filename}.obj'

            f = open(output_file_location, 'w')
            while i < 100:
                f.write(f'{RAM_ASSEMBLER[i]} {RAM_ASSEMBLER[i + 1]}\n')
                i += 2
            f.close()

            # Runs simulator using generated .obj file
            self.load_micro_sim_ram(output_file_location)

        except (AssertionError, FileNotFoundError, ValueError, MemoryError, KeyError, SyntaxError) as e:
            toast(f'{e}')

    def load_micro_sim_ram(self, file):
        """
        Loads microprocessor simulator ram with the contents of specified file
        :param file: str
        """
        self.micro_sim.read_obj_file(file)

    def clear_dialog(self, instance):
        """
        Dialog box warning user if they wish to clear all content prior to saving
        :param instance: obj
        """
        if EVENTS['EDITOR_SAVED']:
            self.clear()
        elif EVENTS['IS_RAM_EMPTY']:
            toast('There is nothing to clear')
        else:
            dialog = MDDialog(title='Warning',
                              text='Are you sure you want to clear without saving?',
                              size_hint=(.3, .3),
                              text_button_ok='Clear',
                              text_button_cancel='Cancel',
                              events_callback=self.clear_decision)
            if self.dpi >= 192:
                dialog.pos_hint = {
                    'x': dp(0.18),
                    'y': dp(0.18)
                }
            dialog.open()

    def clear_decision(self, *args):
        """
        User decision from [clear_dialog].
        :param *args: tuple
        """
        if args[0] == 'Clear':
            self.clear()
        else:
            toast('Please save your changes')

    def clear(self):
        """
        Clears all data from app
        """
        if EVENTS['IS_RAM_EMPTY']:
            toast('There is nothing to clear')
        else:
            self.step_index = 0
            clear_ram()
            EVENTS['FILE_PATH'] = ''
            EVENTS['LOADED_FILE'] = False
            self.run_window.editor.clear()
            self.micro_sim.micro_clear()
            self.run_window.reg_table.data_list.clear()
            self.run_window.inst_table.data_list.clear()

            self.run_window.inst_table.get_data(self.micro_sim.index,
                                                self.micro_sim.disassembled_instruction())
            self.run_window.event_data_tables()

            self.first_inst = True

            self.run_window.blinking_on.cancel()
            self.run_window.blinking_off.cancel()

            self.run_window.event_io()
            toast('Micro memory cleared! Load new data')
            EVENTS['IS_RAM_EMPTY'] = True
            update_indicators(self, EVENTS['LOADED_FILE'])
            EVENTS['IS_OBJ'] = False
            self.run_window.editor.disabled = False

    def clear_run(self):
        """
        Clears all data for microprocessor execution
        """
        self.step_index = 0
        clear_ram()
        self.micro_sim.micro_clear()
        self.run_window.inst_table.data_list.clear()

        self.run_window.inst_table.get_data(self.micro_sim.index,
                                            self.micro_sim.disassembled_instruction())
        self.first_inst = True

        self.run_window.blinking_on.cancel()
        self.run_window.blinking_off.cancel()
        self.run_window.event_data_tables()
        self.run_window.event_io()

    def open_reg_mem_save_dialog(self, instance):
        """
        It will be called when user click on the save file button.
        :param instance: obj
        """
        dialog = MDInputDialog(title='Save file: Enter file name',
                               hint_text='Enter file name',
                               size_hint=(.3, .3),
                               text_button_ok='Save',
                               text_button_cancel='Cancel',
                               events_callback=self.save_file)
        if self.dpi >= 192:
            dialog.pos_hint = {
                'x': dp(0.18),
                'y': dp(0.18)
            }
        toast('Save Register and Memory Content')
        dialog.open()

    def open_editor_save_dialog(self, instance):
        """
        Opens code editor save dialog
        :param instance: obj
        """
        if EVENTS['IS_OBJ']:
            toast('Obj files cannot be modified.')
        elif EVENTS['LOADED_FILE']:
            self.run_window.editor.save(EVENTS['FILE_PATH'])
            toast('Content saved on loaded file')
            EVENTS['EDITOR_SAVED'] = True
        else:
            dialog = MDInputDialog(title='Save file: Enter file name',
                                   hint_text='Enter file name',
                                   size_hint=(.3, .3),
                                   text_button_ok='Save',
                                   text_button_cancel='Cancel',
                                   events_callback=self.save_asm_file)
            if self.dpi >= 192:
                dialog.pos_hint = {
                    'x': dp(0.18),
                    'y': dp(0.18)
                }
            toast('Save Editor Content')
            dialog.open()

    def save_asm_file(self, *args):
        """
        Saves asm file
        :param args: tuple
        """
        if args[0] == 'Save':
            filename = args[0]

            # Checks if user input is valid or null for filename. if null, assigns a default filename
            if args[1].text_field.text:
                filename = args[1].text_field.text

            self.run_window.editor.save(f'input/{filename}.asm')
            toast(f'File saved in input folder as {filename}.asm')
            EVENTS['EDITOR_SAVED'] = True
            EVENTS['FILE_PATH'] = f'input/{filename}.asm'
            EVENTS['LOADED_FILE'] = True
            update_indicators(self, EVENTS['LOADED_FILE'])
        else:
            toast('File save cancelled')

    def save_file(self, *args):
        """
        It is called when user clicks on 'Save' or 'Cancel' button of dialog.
        Saves file.
        :param *args: obj
        """
        if args[0] == 'Save':
            filename = args[0]

            # Checks if user input is valid or null for filename. if null, assigns a default filename
            if args[1].text_field.text:
                filename = args[1].text_field.text

            f = open(f'output/{filename}.txt', 'w')
            f.write('\nRegister Content: \n')
            for k, v in REGISTER.items():
                f.write(f'\nk.upper():       {v.upper()}\n')

            i = 0
            f.write('\nMemory Content: \n')
            while i < 100:
                f.write(f'\n{RAM[i]}    {RAM[i + 1]}')
                i += 2

            toast(f'File saved in output folder as {filename.txt}')
            f.close()

        else:
            toast('File save cancelled')

    def buttons_information(self, instance):
        """
        It is called when user clicks on information buttons.
        :param instance:
        """
        if instance.icon == 'file-alert':
            toast('No file loaded yet')
        if instance.icon == 'file-check':
            toast(f"File at '{EVENTS['FILE_PATH']}' loaded")


class NavDrawer(MDNavigationDrawer):
    """Main menu of application"""

    def __init__(self, **kwargs):
        self.micro_sim = kwargs.pop('micro_sim')
        self.app = kwargs.pop('app')
        self.dpi = kwargs.pop('dpi')
        self.main_window = kwargs.pop('main_window')
        super().__init__(**kwargs)
        self.drawer_logo = 'assets/images/logo.jpg'
        self.spacing = 0
        self.manager_open = False
        self.manager = None
        self.history = []

        self.add_widget(NavigationDrawerSubheader(text='Menu:'))
        self.add_widget(NavigationDrawerIconButton(icon='paperclip',
                                                   text='Load File',
                                                   on_release=self.file_manager_open))
        self.add_widget(NavigationDrawerIconButton(icon='traffic-light',
                                                   text=TRAFFIC_LIGHT['menu_title'] + '. Current Port: ' + str(
                                                       TRAFFIC_LIGHT['port']),
                                                   on_release=self.io_config_open))
        self.add_widget(NavigationDrawerIconButton(icon='numeric-7-box-multiple',
                                                   text=SEVEN_SEGMENT_DISPLAY['menu_title'] + '. Current Port: ' + str(
                                                       SEVEN_SEGMENT_DISPLAY['port']),
                                                   on_release=self.io_config_open))
        self.add_widget(NavigationDrawerIconButton(icon='alphabetical-variant',
                                                   text=ASCII_TABLE['menu_title'] + '. Current Port: ' + str(
                                                       ASCII_TABLE['port']),
                                                   on_release=self.io_config_open))
        self.add_widget(NavigationDrawerIconButton(icon='keyboard',
                                                   text=HEX_KEYBOARD['menu_title'] + '. Current Port: ' + str(
                                                       HEX_KEYBOARD['port']),
                                                   on_release=self.io_config_open))

    def io_config_open(self, instance):
        """
        Opens IO configuration dialog
        :param instance: obj
        """
        dialog = MDInputDialog(title=instance.text,
                               hint_text='Input port number [0-4095]',
                               text_button_ok='Save',
                               text_button_cancel='Cancel',
                               size_hint=(dp(0.4), dp(0.4)),
                               events_callback=self.save_io_ports)
        if self.dpi >= 192:
            dialog.size_hint = (dp(0.2), dp(0.2))
            dialog.pos_hint = {
                'x': dp(0.15),
                'y': dp(0.15)
            }
        dialog.open()

    def save_io_ports(self, *args):
        """
        Saves IO port configurations
        :param args: tuple
        """
        if args[0] == 'Save':
            title = args[1].title
            text = args[1].text_field.text
            if text.isdigit():
                port = int(text)
                if port < 0 or port > 4095:
                    toast('Invalid port number. Valid port numbers [0-4095]')
                else:
                    self.update_io_port(title, port)
            else:
                toast('Invalid input. Not a number!')

    def update_io_port(self, title, port):
        """
        Updates IO port for specified IO
        :param title: str
        :param port: int
        """
        if is_valid_port(port):
            if title == TRAFFIC_LIGHT['menu_title']:
                update_reserved_ports(TRAFFIC_LIGHT,
                                      TRAFFIC_LIGHT['port'],
                                      port)
                toast_message = f'Changed Traffic Light I/O port number to {port}'
            elif title == SEVEN_SEGMENT_DISPLAY['menu_title']:
                update_reserved_ports(SEVEN_SEGMENT_DISPLAY,
                                      SEVEN_SEGMENT_DISPLAY['port'],
                                      port)
                toast_message = f'Changed Seven Segment I/O port number to {port}'
            elif title == ASCII_TABLE['menu_title']:
                if port > 4088:
                    toast_message = 'Invalid port for ASCII Table. Valid ports [0-4088]'
                else:
                    try:
                        update_reserved_ports(ASCII_TABLE,
                                              ASCII_TABLE['port'],
                                              port, True)
                        toast_message = f'Changed ASCII Table I/O port number to {port}'
                    except MemoryError as e:
                        toast_message = str(e)
            else:
                update_reserved_ports(HEX_KEYBOARD,
                                      HEX_KEYBOARD['port'],
                                      port)
                toast_message = f'Changed HEX Keyboard I/O port number to {port}'
            toast(toast_message)
        else:
            toast('Invalid input. That port is reserved!')

    def file_manager_open(self, instance):
        """
        Opens file manager
        :param instance: obj
        """
        if not self.manager:
            manager_size = (dp(1), 1) if self.dpi < 192 else (dp(0.5), 1)
            self.manager = ModalView(auto_dismiss=False,
                                     size_hint=manager_size,
                                     background_color=[1, 1, 1, 1])
            self.file_manager = MDFileManager(exit_manager=self.exit_manager,
                                              select_path=self.select_path,
                                              ext=['.asm', '.obj'])
            self.manager.add_widget(self.file_manager)
            # output manager to the screen
            self.file_manager.show(str(Path.home()))
        self.manager_open = True
        self.manager.open()
        self.history = self.file_manager.history

    def select_path(self, path):
        """
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: str
        """
        self.exit_manager()

        if path.endswith('.obj'):
            EVENTS['IS_OBJ'] = True
            EVENTS['EDITOR_SAVED'] = True

        EVENTS['CAN_WRITE'] = True
        EVENTS['FILE_PATH'] = path
        EVENTS['LOADED_FILE'] = True
        toast(f'{path} loaded successfully')
        EVENTS['IS_RAM_EMPTY'] = False
        update_indicators(self.main_window, EVENTS['LOADED_FILE'])

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""
        self.manager.dismiss()
        self.manager_open = False
        self.file_manager.history = self.history

    def events(self, instance, keyboard, keycode, text, modifiers):
        """Called when buttons are pressed on the mobile device.."""
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


class RegisterTable(RecycleView):
    """Holds data relevant to registers"""
    data_list = ListProperty([])

    def __init__(self, **kwargs):
        self.dpi = kwargs.pop('dpi')
        super(RegisterTable, self).__init__(**kwargs)
        self.viewclass = 'Label'
        self.recycle_grid_layout = self.children[0]
        if self.dpi < 192:
            self.pos_hint = {
                'x': dp(0),
                'center_y': dp(0.75)
            }
            self.size_hint_x = dp(0.2)
            self.size_hint_y = dp(0.5)
            with self.children[0].canvas.before:
                Color(.50, .50, .50, 1)
                for i in range(13):
                    Line(width=2,
                         rectangle=(dp(0), dp(0), dp(205), dp(390 - (30 * i))))
                Line(width=2, rectangle=(dp(0), dp(0), dp(102.5), dp(390)))
        else:
            self.pos_hint = {
                'x': dp(0),
                'center_y': dp(0.368)
            }
            self.size_hint_x = dp(0.12)
            self.size_hint_y = dp(0.265)
            self.recycle_grid_layout.size_hint_x = dp(0.47)
            with self.children[0].canvas.before:
                Color(.50, .50, .50, 1)
                for i in range(13):
                    Line(width=2,
                         rectangle=(dp(0), dp(0), dp(245), dp(390 - (30 * i))))
                Line(width=2, rectangle=(dp(0), dp(0), dp(115), dp(390)))

    def get_data(self):
        """Updates data inside Register table"""
        _data_list = self.data_list.copy()
        self.data_list.clear()
        self.data_list.append('REGISTER')
        self.data_list.append('VALUE')
        _data = []
        for k, v in REGISTER.items():
            self.data_list.append(k)
            self.data_list.append(v)

        if not self.data:
            for item in self.data_list:
                self.data.append({
                    'text': item.upper(),
                    'color': (.1, .1, .1, 1)
                })
        else:
            i = 0
            while i < len(self.data):
                if self.data[i]['text'] == self.data_list[i].upper() \
                        and self.data[i + 1]['text'] != self.data_list[i + 1]:
                        self.data[i]['color'] = (1, 0, 0, 1)
                        self.data[i + 1]['text'] = self.data_list[i + 1]
                        self.data[i + 1]['color'] = (1, 0, 0, 1)
                else:
                    self.data[i]['color'] = (.1, .1, .1, 1)
                    self.data[i + 1]['color'] = (.1, .1, .1, 1)
                i += 2
            self.refresh_from_data()


class MemoryTable(RecycleView):
    """Holds data relevant to RAM"""
    data_list = ListProperty([])

    def __init__(self, **kwargs):
        self.dpi = kwargs.pop('dpi')
        super(MemoryTable, self).__init__(**kwargs)
        self.viewclass = 'Label'
        self.recycle_grid_layout = self.children[0]
        if self.dpi < 192:
            self.pos_hint = {
                'x': dp(0.75),
                'center_y': dp(0.75)
            }
            self.size_hint_x = dp(0.3)
            self.size_hint_y = dp(0.5)
            self.recycle_grid_layout.default_size_hint = (dp(0.5), None)
            self.recycle_grid_layout.size_hint_x = dp(0.83)
            with self.children[0].canvas.before:
                Color(.50, .50, .50, 1)
                for i in range(51):
                    Line(width=2,
                         rectangle=(dp(0), dp(0), dp(255), dp(1530 - (30 * i))))
                Line(width=2, rectangle=(dp(0), dp(0), dp(127.5), dp(1530)))
        else:
            self.pos_hint = {
                'x': dp(0.37),
                'center_y': dp(0.368)
            }
            self.size_hint_x = dp(0.135)
            self.size_hint_y = dp(0.265)
            self.recycle_grid_layout.default_size_hint = (dp(0.5), None)
            self.recycle_grid_layout.size_hint_x = dp(0.47)
            with self.children[0].canvas.before:
                Color(.50, .50, .50, 1)
                for i in range(51):
                    Line(width=2,
                         rectangle=(dp(0), dp(0), dp(270), dp(1530 - (30 * i))))
                Line(width=2, rectangle=(dp(0), dp(0), dp(135), dp(1530)))

    def get_data(self):
        """Updates data in memory table"""
        self.data_list.append('MEMORY BYTE')
        self.data_list.append('MEMORY BYTE')
        i = 0
        while i < 100:
            self.data_list.append(f'{RAM[i]}')
            self.data_list.append(f'{RAM[i + 1]}')
            i += 2

        self.data = [{
            "text": str(x.upper()),
            "color": (.1, .1, .1, 1)
        } for x in self.data_list]


class InstructionTable(RecycleView):
    """Holds relevant data to Instructions table"""
    data_list = ListProperty([])

    def __init__(self, **kwargs):
        self.dpi = kwargs.pop('dpi')
        super(InstructionTable, self).__init__(**kwargs)
        self.viewclass = 'Label'
        if self.dpi < 192:
            self.pos_hint = {
                'x': dp(0.2),
                'center_y': dp(0.75)
            }
            self.size_hint_x = dp(1)
            self.size_hint_y = dp(0.5)
        else:
            self.pos_hint = {
                'x': dp(0.12),
                'center_y': dp(0.368)
            }
            self.size_hint_x = dp(0.25)
            self.size_hint_y = dp(0.265)

    def get_data(self, address, instruction):
        """
        Updates data in Instructions table
        :param address: str
        :param instruction: str
        """
        if not self.data_list:
            self.data_list.append('ADDRESS')
            self.data_list.append('CONTENT')
            self.data_list.append('DISASSEMBLY')
        else:
            self.data_list.append((f'{address:02x}').upper())
            self.data_list.append(f'{RAM[address]}')
            self.data_list.append(instruction.upper())

        self.data = [{
            "text": str(x.upper()),
            "color": (.1, .1, .1, 1)
        } for x in self.data_list]


class TextEditor(CodeInput):
    """Application text editor for assembly code"""

    def __init__(self, **kwargs):
        self.dpi = kwargs.pop('dpi')
        super(TextEditor, self).__init__(**kwargs)
        self.bind(text=self.on_text)
        self.valid_text = False
        self.lexer = SemrefLexer()
        self.font_name = 'assets/fonts/Inconsolata-Regular.ttf'
        if self.dpi < 192:
            self.size_hint = (0.55, 0.46)
            self.pos_hint = {
                'x': dp(0.20),
                'y': dp(0.04)
            }
        else:
            self.size_hint = (0.50, 0.43)
            self.pos_hint = {
                'x': dp(0.12),
                'y': dp(0.02)
            }

    def on_text(self, instance, value):
        """
        On text change reapply syntax highlighting on keywords
        :param instance: obj
        :param value: str
        """
        if not EVENTS['IS_OBJ']:
            EVENTS['EDITOR_SAVED'] = False

        if value:
            self.valid_text = True
            EVENTS['IS_RAM_EMPTY'] = False
        else:
            self.valid_text = False

    def load_file(self, file_path):
        """
        Loads file into text editor
        :param file_path: str
        """
        if EVENTS['IS_OBJ']:
            self.disabled = True
        else:
            self.disabled = False
            with open(file_path, 'r') as file:
                data = file.read()
                file.close()
            self.text = data
            EVENTS['EDITOR_SAVED'] = True

    def clear(self):
        """
        Clears text in text editor
        """
        self.text = ''
        self.valid_text = False

    def save(self, file_path):
        """
        Save contents of code editor in a file
        :param file_path: str
        """
        with open(file_path, 'w') as file:
            file.write(self.text)
            file.close()


class GUI(NavigationLayout):
    """Main layout used to display user interface"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.micro_sim = MicroSim()
        self.dpi = MetricsBase().dpi
        self.main_window = MainWindow(nav_drawer=self,
                                      app=self.app,
                                      micro_sim=self.micro_sim,
                                      dpi=self.dpi)
        self.add_widget(NavDrawer(micro_sim=self.micro_sim,
                                  app=self.app,
                                  dpi=self.dpi, main_window=self.main_window))
        self.add_widget(self.main_window)


class SemrefApp(App):
    """Main application"""
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'BlueGray'
    theme_cls.accent_palette = 'Orange'

    def build(self):
        """Initializes app with a widget tree"""
        return GUI()
