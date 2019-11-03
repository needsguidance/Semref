from pathlib import Path
from queue import Queue
from threading import Lock, Thread, Semaphore, Condition
from time import sleep

from kivy.metrics import dp, sp

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.properties import (ListProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
from kivymd.theming import ThemeManager
from kivymd.toast import toast
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFlatButton
from kivymd.uix.dialog import MDInputDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.navigationdrawer import (MDNavigationDrawer, MDToolbar,
                                         NavigationDrawerIconButton,
                                         NavigationDrawerSubheader,
                                         NavigationLayout)

from constants import REGISTER, hex_to_binary, convert_to_hex, is_valid_port, update_reserved_ports
from constants import TRAFFIC_LIGHT, SEVEN_SEGMENT_DISPLAY, ASCII_TABLE, HEX_KEYBOARD
from microprocessor_simulator import MicroSim, RAM


class HexKeyboard(GridLayout):

    def __init__(self, **kwargs):
        self.mem_table = kwargs.pop('mem_table')
        self.light = kwargs.pop('light')
        self.micro_sim = kwargs.pop('micro_sim')
        self.event_on = kwargs.pop('event_on')
        self.event_off = kwargs.pop('event_off')

        super(HexKeyboard, self).__init__(**kwargs)
        self.cols = 4
        self.size_hint = (dp(0.4), dp(0.4))
        self.pos_hint = {'x': dp(0.30), 'y': dp(0.35)}
        self.queue = Queue(maxsize=10)
        self.lock = Lock()
        self.semaphore = Semaphore()
        self.condition = Condition()

        with self.canvas.before:
            Color(.50, .50, .50, 1)
            Rectangle(pos=(dp(303), dp(72)), size=(dp(362), dp(208)))

        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=(dp(307), dp(77)), size=(dp(354), dp(199)))

            Color(.75, .75, .75, 1)
            Rectangle(pos=(dp(307), dp(76)), size=(dp(353), dp(143)))

            Color(.50, .50, .50, 1)
            Line(rectangle=(dp(307), dp(183), dp(87), dp(35)), width=dp(dp(0.8)))

            Line(rectangle=(dp(396), dp(183), dp(87), dp(35)), width=dp(dp(0.8)))

            Line(rectangle=(dp(485), dp(183), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(574), dp(183), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(307), dp(148), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(396), dp(148), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(485), dp(148), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(574), dp(148), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(307), dp(113), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(396), dp(113), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(485), dp(113), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(574), dp(113), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(307), dp(78), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(396), dp(78), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(485), dp(78), dp(87), dp(35)), width=dp(0.8))

            Line(rectangle=(dp(574), dp(78), dp(87), dp(35)), width=dp(0.8))

        for i in range(16):
            if i > 9:
                i = str(chr(i + 55))
            self.add_widget(MDFlatButton(text=f'{i}',
                                         on_release=self.hex_key_press))

    def hex_key_press(self, instance):
        """
        On hex keyboard press, a thread verifies if RAM is ready to be written. Uses a shared queue to enqueue pressed
        keys that are to be written to RAM.
        :param instance: obj
        """
        thread = Thread(target=self.is_ram_ready)
        if not self.queue.full():
            self.queue.put(hex_to_binary(instance.text))
            thread.start()

    def is_ram_ready(self):
        """
        Utilizes semaphores and monitors to prevent threads from writing to RAM at the same time. Current thread is
        allowed to write to RAM if the LSB is 0, otherwise it must wait.
        """
        with self.semaphore:
            binary = hex_to_binary(RAM[HEX_KEYBOARD['port']])
            if binary[-1] != 0:
                self.condition.acquire()
            self.write_ram()

    def write_ram(self):
        with self.lock:
            RAM[HEX_KEYBOARD['port']] = convert_to_hex(
                int(f'{self.queue.get()}0001', 2), 8)

            self.mem_table.data_list.clear()
            self.mem_table.get_data()

            self.event_on.cancel()
            self.event_off.cancel()

            self.event_on()
            self.event_off()
            sleep(1)
            self.condition.release()


class RunWindow(FloatLayout):

    def __init__(self, **kwargs):
        self.app = kwargs.pop('app')
        self.micro_sim = kwargs.pop('micro_sim')
        self.step_index = 0
        self.header = False
        self.first_inst = True
        super(RunWindow, self).__init__(**kwargs)
        self.run_button = MDFillRoundFlatIconButton(text='Run',
                                                    icon='run',
                                                    size_hint=(None, None),
                                                    pos_hint={
                                                        'center_x': dp(.7), 'center_y': dp(2.12)},
                                                    on_release=self.run_micro_instructions)
        self.debug_button = MDFillRoundFlatIconButton(text='Debug',
                                                      icon='android-debug-bridge',
                                                      size_hint=(None, None),
                                                      pos_hint={
                                                          'center_x': dp(.9), 'center_y': dp(2.12)},
                                                      on_release=self.run_micro_instructions_step)
        self.refresh_button = MDFillRoundFlatIconButton(text='Clear',
                                                        icon='refresh',
                                                        size_hint=(None, None),
                                                        pos_hint={
                                                            'center_x': dp(.5), 'center_y': dp(2.12)},
                                                        on_release=self.clear)
        self.save_button = MDFillRoundFlatIconButton(text='Save File',
                                                     icon='download',
                                                     size_hint=(None, None),
                                                     pos_hint={
                                                         'center_x': dp(.35), 'center_y': dp(2.12)},
                                                     on_release=self.open_save_dialog)

        self.ascii_label_1 = Label(text='[color=000000]' + chr(int(RAM[4088], 16)) + '[/color]', pos=(dp(-187), dp(-105)),
                                   font_size=sp(40), markup=True)
        self.ascii_label_2 = Label(text='[color=000000]' + chr(int(RAM[4089], 16)) + '[/color]', pos=(dp(-146), dp(-105)),
                                   font_size=sp(40), markup=True)
        self.ascii_label_3 = Label(text='[color=000000]' + chr(int(RAM[4090], 16)) + '[/color]', pos=(dp(-100), dp(-105)),
                                   font_size=sp(40), markup=True)
        self.ascii_label_4 = Label(text='[color=000000]' + chr(int(RAM[4091], 16)) + '[/color]', pos=(dp(-54), dp(-105)),
                                   font_size=sp(40), markup=True)
        self.ascii_label_5 = Label(text='[color=000000]' + chr(int(RAM[4092], 16)) + '[/color]', pos=(dp(-8), dp(-105)),
                                   font_size=sp(40), markup=True)
        self.ascii_label_6 = Label(text='[color=000000]' + chr(int(RAM[4093], 16)) + '[/color]', pos=(dp(38), dp(-105)),
                                   font_size=sp(40), markup=True)
        self.ascii_label_7 = Label(text='[color=000000]' + chr(int(RAM[4094], 16)) + '[/color]', pos=(dp(84), dp(-105)),
                                   font_size=sp(40), markup=True)
        self.ascii_label_8 = Label(text='[color=000000]' + chr(int(RAM[4095], 16)) + '[/color]', pos=(dp(130), dp(-105)),
                                   font_size=sp(40), markup=True)

        self.ascii = ASCIIGrid()
        self.reg_table = RegisterTable()
        self.mem_table = MemoryTable()
        self.inst_table = InstructionTable()
        self.light = TrafficLights()
        self.seven_segment_display = SevenSegmentDisplay()

        self.reg_table.get_data()
        self.mem_table.data_list.clear()
        self.mem_table.get_data()
        self.inst_table.get_data(
            self.micro_sim.index, self.header, self.micro_sim.disassembled_instruction())
        self.header = True
        self.hex_keyboard_label = Label(text='HEX KEYBOARD',
                                        font_size=sp(20),
                                        color=(0, 0, 0, 1),
                                        # size_hint=(1, 0.17),
                                        pos_hint={'x': dp(-0.025), 'y': dp(0.35)})

        # Create variable of scheduling instance so that it can be turned on and off,
        # to avoid repeat of the same thread
        self.event_on = Clock.schedule_interval(
            self.light.intermittent_off, 0.5)
        self.event_off = Clock.schedule_interval(
            self.light.intermittent_on, 0.3)

        # Creates a clock thread that updates all tables and i/o's every 0.2 seconds. Does not get cancelled.
        self.event_io = Clock.schedule_interval(self.update_io, 0.2)

        # Since the instancing of the events actually starts the scheduling, needs to be canceled right away
        self.event_on.cancel()
        self.event_off.cancel()

        self.hex_keyboard_layout = HexKeyboard(mem_table=self.mem_table, light=self.light,
                                               micro_sim=self.micro_sim, event_on=self.event_on,
                                               event_off=self.event_off)
        self.add_widget(self.save_button)
        self.add_widget(self.run_button)
        self.add_widget(self.debug_button)
        self.add_widget(self.refresh_button)
        self.add_widget(self.reg_table)
        self.add_widget(self.inst_table)
        self.add_widget(self.mem_table)
        self.add_widget(self.light)
        self.add_widget(self.hex_keyboard_layout)
        self.add_widget(self.hex_keyboard_label)
        self.add_widget(self.seven_segment_display)
        self.add_widget(self.ascii)
        self.add_widget(self.ascii_label_1)
        self.add_widget(self.ascii_label_2)
        self.add_widget(self.ascii_label_3)
        self.add_widget(self.ascii_label_4)
        self.add_widget(self.ascii_label_5)
        self.add_widget(self.ascii_label_6)
        self.add_widget(self.ascii_label_7)
        self.add_widget(self.ascii_label_8)

    def open_save_dialog(self, instance):
        """It will be called when user click on the save file button.

        :param instance: used as event handler for button click;

        """
        dialog = MDInputDialog(
            title='Save file: Enter file name', hint_text='Enter file name', size_hint=(.3, .3),
            text_button_ok='Save',
            text_button_cancel='Cancel',
            events_callback=self.save_file)
        toast('Save Register and Memory Content')
        dialog.open()

    def save_file(self, *args):
        """It is called when user clicks on 'Save' or 'Cancel' button of dialog.

        :type *args: object array
        :param *args: passes an object array generated when opening open_save_dialog. 
                Said object indcludes input text used for file saving;

        """
        if args[0] == 'Save':
            filename = args[0]

            # Checks if user input is valid or null for filename. if null, assigns a default filename
            if args[1].text_field.text:
                filename = args[1].text_field.text

            f = open('output/' + filename + '.txt', 'w')
            f.write('\nRegister Content: \n')
            for k, v in REGISTER.items():
                f.write('\n' + k.upper() + ':' + '       ' + v.upper() + '\n')

            i = 0
            f.write('\nMemory Content: \n')
            for m in range(50):
                f.write(f'\n{RAM[i]}    {RAM[i + 1]}')
                i += 2

            toast('File saved in output folder as ' + filename + '.txt')
            f.close()

        else:
            toast('File save cancelled')

    def run_micro_instructions(self, instance):
        if not self.micro_sim.is_running:
            toast('Infinite loop encountered. Program stopped')
        else:
            if not self.micro_sim.is_ram_loaded:
                toast('Must load file first before running')
            else:
                for m in range(2):
                    if self.first_inst:
                        self.inst_table.data_list.clear()
                        self.header = False
                        self.inst_table.get_data(self.micro_sim.index, self.header,
                                                 self.micro_sim.disassembled_instruction())
                        self.header = True
                        self.inst_table.get_data(self.micro_sim.index, self.header,
                                                 self.micro_sim.disassembled_instruction())
                        self.first_inst = False
                    else:
                        self.micro_sim.prev_index = -1
                        self.event_on.cancel()
                        self.event_off.cancel()
                        self.reg_table.get_data()
                        self.mem_table.data_list.clear()
                        self.mem_table.get_data()
                        self.event_on()
                        self.event_off()

                        while self.micro_sim.is_running:
                            self.micro_sim.run_micro_instructions()
                            self.inst_table.get_data(self.micro_sim.index, self.header,
                                                     self.micro_sim.disassembled_instruction())

                            if self.micro_sim.prev_index == self.micro_sim.index:
                                self.micro_sim.is_running = False
                            else:
                                self.micro_sim.prev_index = self.micro_sim.index

                toast('File executed successfully')
                for i in self.micro_sim.micro_instructions:
                    if i != 'NOP':
                        print(i)

    def update_io(self, dt):
        self.light.change_color(self.micro_sim.traffic_lights_binary())
        self.seven_segment_display.activate_segments(
            self.micro_sim.seven_segment_binary())
        self.update_ascii_grid()

    def clear(self, instance):
        self.header = False
        self.step_index = 0
        self.micro_sim.micro_clear()
        self.reg_table.data_list.clear()
        self.reg_table.get_data()
        self.mem_table.data_list.clear()
        self.mem_table.get_data()
        self.inst_table.data_list.clear()
        self.inst_table.get_data(
            self.micro_sim.index, self.header, self.micro_sim.disassembled_instruction())
        self.header = True
        self.first_inst = True

        # Cancels last scheduling thread for clean event
        self.event_on.cancel()
        self.event_off.cancel()

        self.light.change_color(self.micro_sim.traffic_lights_binary())
        self.update_ascii_grid()
        self.seven_segment_display.activate_segments(
            self.micro_sim.seven_segment_binary())
        toast('Micro memory cleared! Load new data')

    def run_micro_instructions_step(self, instance):
        if not self.micro_sim.is_running:
            toast("Infinite loop encountered. Program stopped")
        else:
            if not self.micro_sim.is_ram_loaded:
                toast('Must load file first before running')
            else:
                self.step_index += 1
                if self.first_inst:
                    self.inst_table.get_data(self.micro_sim.index, self.header,
                                             self.micro_sim.disassembled_instruction())
                    self.first_inst = False

                else:
                    self.reg_table.get_data()
                    self.mem_table.data_list.clear()
                    self.mem_table.get_data()
                    self.micro_sim.run_micro_instructions_step(self.step_index)

                    self.inst_table.get_data(self.micro_sim.index, self.header,
                                             self.micro_sim.disassembled_instruction())

                toast('Runnin instruction in step-by-step mode. Step ' +
                      str(self.step_index) + ' is running')
                for i in self.micro_sim.micro_instructions:
                    if i != 'NOP':
                        print(i)

    def update_ascii_grid(self):
        self.ascii_label_1.text = '[color=000000]' + \
            chr(int(RAM[ASCII_TABLE['port']], 16)) + '[/color]'
        self.ascii_label_2.text = '[color=000000]' + \
            chr(int(RAM[ASCII_TABLE['port'] + 1], 16)) + '[/color]'
        self.ascii_label_3.text = '[color=000000]' + \
            chr(int(RAM[ASCII_TABLE['port'] + 2], 16)) + '[/color]'
        self.ascii_label_4.text = '[color=000000]' + \
            chr(int(RAM[ASCII_TABLE['port'] + 3], 16)) + '[/color]'
        self.ascii_label_5.text = '[color=000000]' + \
            chr(int(RAM[ASCII_TABLE['port'] + 4], 16)) + '[/color]'
        self.ascii_label_6.text = '[color=000000]' + \
            chr(int(RAM[ASCII_TABLE['port'] + 5], 16)) + '[/color]'
        self.ascii_label_7.text = '[color=000000]' + \
            chr(int(RAM[ASCII_TABLE['port'] + 6], 16)) + '[/color]'
        self.ascii_label_8.text = '[color=000000]' + \
            chr(int(RAM[ASCII_TABLE['port'] + 7], 16)) + '[/color]'


class MainWindow(BoxLayout):

    def __init__(self, **kwargs):
        self.nav_drawer = kwargs.pop('nav_drawer')
        self.app = kwargs.pop('app')
        self.micro_sim = kwargs.pop('micro_sim')
        super().__init__(**kwargs)
        self.ids['left_actions'] = BoxLayout()
        self.orientation = 'vertical'
        self.add_widget(MDToolbar(title='Semref Micro Sim',
                                  md_bg_color=self.app.theme_cls.primary_color,
                                  background_palette='Primary',
                                  background_hue='500',
                                  elevation=10,
                                  ids=self.ids,
                                  left_action_items=[['dots-vertical', lambda x: self.nav_drawer.toggle_nav_drawer()]]))

        self.add_widget(BoxLayout())  # Bumps up navigation bar to the top
        self.add_widget(RunWindow(app=self.app, micro_sim=self.micro_sim))


class NavDrawer(MDNavigationDrawer):

    def __init__(self, **kwargs):
        self.micro_sim = kwargs.pop('micro_sim')
        super().__init__(**kwargs)
        self.drawer_logo = 'images/logo.jpg'
        self.manager_open = False
        self.manager = None
        self.light = TrafficLights()

        self.add_widget(NavigationDrawerSubheader(text='Menu:'))
        self.add_widget(NavigationDrawerIconButton(icon='paperclip',
                                                   text='Load File',
                                                   on_release=self.file_manager_open))
        self.add_widget(NavigationDrawerIconButton(icon='traffic-light',
                                                   text=TRAFFIC_LIGHT['menu_title'],
                                                   on_release=self.io_config_open))
        self.add_widget(NavigationDrawerIconButton(icon='numeric-7-box-multiple',
                                                   text=SEVEN_SEGMENT_DISPLAY['menu_title'],
                                                   on_release=self.io_config_open))
        self.add_widget(NavigationDrawerIconButton(icon='alphabetical-variant',
                                                   text=ASCII_TABLE['menu_title'],
                                                   on_release=self.io_config_open))
        self.add_widget(NavigationDrawerIconButton(icon='keyboard',
                                                   text=HEX_KEYBOARD['menu_title'],
                                                   on_release=self.io_config_open))

    def io_config_open(self, instance):
        dialog = MDInputDialog(title=instance.text,
                               hint_text='Input port number [0-4095]',
                               size_hint=(dp(0.8), dp(0.4)),
                               text_button_ok='Save',
                               text_button_cancel='Cancel',
                               events_callback=self.save_io_ports)
        dialog.open()

    def save_io_ports(self, *args):
        if args[0] == 'Save':
            title = args[1].title
            text = args[1].text_field.text
            if text.isdigit():
                port = int(text)
                if port < 0 or port > 4095:
                    toast('Invalid port number. Valid port numbers [0-4095]')
                else:
                    if is_valid_port(port):
                        if title == TRAFFIC_LIGHT['menu_title']:
                            update_reserved_ports(
                                TRAFFIC_LIGHT, TRAFFIC_LIGHT['port'], port)
                            toast_message = 'Changed Traffic Light I/O port number to ' + \
                                str(port)

                        elif title == SEVEN_SEGMENT_DISPLAY['menu_title']:
                            update_reserved_ports(
                                SEVEN_SEGMENT_DISPLAY, SEVEN_SEGMENT_DISPLAY['port'], port)
                            toast_message = 'Changed Seven Segment I/O port number to ' + \
                                str(port)

                        elif title == ASCII_TABLE['menu_title']:
                            if port > 4088:
                                toast_message = 'Invalid port for ASCII Table. Valid ports [0-4088]'
                            else:
                                update_reserved_ports(
                                    ASCII_TABLE, ASCII_TABLE['port'], port)
                                ASCII_TABLE['port'] = port
                                toast_message = 'Changed ASCII Table I/O port number to ' + \
                                    str(port)

                        else:
                            update_reserved_ports(
                                HEX_KEYBOARD, HEX_KEYBOARD['port'], port)
                            HEX_KEYBOARD['port'] = port
                            toast_message = 'Changed HEX Keyboard I/O port number to ' + \
                                str(port)

                        toast(toast_message)
                    else:
                        toast('Invalid input. That port is reserved!')

            else:
                toast('Invalid input. Not a number!')

    def file_manager_open(self, instance):
        if not self.manager:
            self.manager = ModalView(size_hint=(
                dp(1), dp(1)), auto_dismiss=False)
            self.file_manager = MDFileManager(exit_manager=self.exit_manager,
                                              select_path=self.select_path,
                                              ext=['.asm', '.obj'])
            self.manager.add_widget(self.file_manager)
            # output manager to the screen
            self.file_manager.show(str(Path.home()))
        self.manager_open = True
        self.manager.open()

    def select_path(self, path):
        """It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;

        """
        self.exit_manager()
        self.run_micro_sim(path)
        toast(f'{path} loaded successfully')

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""

        self.manager.dismiss()
        self.manager_open = False

    def events(self, instance, keyboard, keycode, text, modifiers):
        """Called when buttons are pressed on the mobile device.."""

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def run_micro_sim(self, file):
        self.micro_sim.read_obj_file(file)


class RegisterTable(RecycleView):
    data_list = ListProperty([])

    def __init__(self, **kwargs):
        super(RegisterTable, self).__init__(**kwargs)
        self.viewclass = 'Label'

    def get_data(self):
        _data_list = self.data_list.copy()
        self.data_list.clear()
        self.data_list.append('REGISTER')
        self.data_list.append('VALUE')
        _data = []
        for k, v in REGISTER.items():
            self.data_list.append(k)
            self.data_list.append(v)

        i = 0
        for j in range(int(len(self.data_list) / 2)):
            if _data_list and len(_data_list) > 2 and _data_list[i] == self.data_list[i] and _data_list[i + 1] != \
                    self.data_list[i + 1]:
                _data.append({'text': self.data_list[i].upper(), 'color': (
                    177 / 255, 62 / 255, 88 / 255, 1)})
                _data.append(
                    {'text': self.data_list[i + 1].upper(), 'color': (177 / 255, 62 / 255, 88 / 255, 1)})
            else:
                _data.append(
                    {'text': self.data_list[i].upper(), 'color': (.1, .1, .1, 1)})
                _data.append(
                    {'text': self.data_list[i + 1].upper(), 'color': (.1, .1, .1, 1)})
            i += 2

        self.data = _data


class MemoryTable(RecycleView):
    data_list = ListProperty([])

    def __init__(self, **kwargs):
        super(MemoryTable, self).__init__(**kwargs)
        self.viewclass = 'Label'

    def get_data(self):
        self.data_list.append('MEMORY BYTE')
        self.data_list.append('MEMORY BYTE')
        i = 0
        for m in range(50):
            self.data_list.append(f'{RAM[i]}')
            self.data_list.append(f'{RAM[i + 1]}')
            i += 2

        self.data = [{"text": str(x.upper()), "color": (.1, .1, .1, 1)}
                     for x in self.data_list]


class InstructionTable(RecycleView):
    data_list = ListProperty([])

    def __init__(self, **kwargs):
        super(InstructionTable, self).__init__(**kwargs)
        self.viewclass = 'Label'

    def get_data(self, address, header, instruction):
        if not header:
            self.data_list.append('ADDRESS')
            self.data_list.append('CONTENT')
            self.data_list.append('DISASSEMBLED INSTRUCTION')
        else:
            self.data_list.append((f'{address:02x}').upper())
            self.data_list.append(f'{RAM[address]}')
            self.data_list.append(instruction.upper())

        self.data = [{"text": str(x.upper()), "color": (.1, .1, .1, 1)}
                     for x in self.data_list]


class TrafficLights(Widget):
    red_1 = ListProperty([1, 0, 0])
    red_2 = ListProperty([1, 0, 0])
    yellow_1 = ListProperty([1, 1, 0])
    yellow_2 = ListProperty([1, 1, 0])
    green_1 = ListProperty([0, 1, 0])
    green_2 = ListProperty([0, 1, 0])

    def __init__(self, **kwargs):
        super(TrafficLights, self).__init__(**kwargs)
        # Index of last bits of the byte used as Input for traffic lights
        self.control_bit_1 = 6
        self.control_bit_2 = 7
        self.binary = ''  # variable needed for intermittent function

    # Scheduler calls method to turn off all lights
    # Parameter dt is the scheduling time
    def intermittent_off(self, dt):
        # First traffic light
        if self.binary[self.control_bit_1] == '1' and self.binary[self.control_bit_2] == '1':
            if self.binary[0] == '1':
                self.red_2 = (0, 0, 0)
            if self.binary[1] == '1':
                self.yellow_2 = (0, 0, 0)
            if self.binary[2] == '1':
                self.green_2 = (0, 0, 0)
        # Second traffic ligth
            if self.binary[3] == '1':
                self.red_1 = (0, 0, 0)
            if self.binary[4] == '1':
                self.yellow_1 = (0, 0, 0)
            if self.binary[5] == '1':
                self.green_1 = (0, 0, 0)

    # Scheduler calls method to turn on all lights
    # Parameter dt is the scheduling time
    def intermittent_on(self, dt):

        # First traffic light
        if self.binary[self.control_bit_1] == '1' and self.binary[self.control_bit_2] == '1':
            if self.binary[0] == '1':
                self.red_2 = (1, 0, 0)
            if self.binary[1] == '1':
                self.yellow_2 = (1, 1, 0)
            if self.binary[2] == '1':
                self.green_2 = (0, 1, 0)
        # Second traffic ligth
            if self.binary[3] == '1':
                self.red_1 = (1, 0, 0)
            if self.binary[4] == '1':
                self.yellow_1 = (1, 1, 0)
            if self.binary[5] == '1':
                self.green_1 = (0, 1, 0)

    # Iterates through the binary at the Input location (RAM) to determine which are 1s and which are 0s
    # Then, changes colors accordingly.
    def change_color(self, binary):
        self.binary = binary
        for bit in range(len(binary)):

            # First traffic ligth
            if bit == 0:
                if binary[bit] == '0':
                    self.red_2 = (0, 0, 0)
                else:
                    self.red_2 = (1, 0, 0)
            elif bit == 1:
                if binary[bit] == '0':
                    self.yellow_2 = (0, 0, 0)
                else:
                    self.yellow_2 = (1, 1, 0)
            elif bit == 2:
                if binary[bit] == '0':
                    self.green_2 = (0, 0, 0)
                else:
                    self.green_2 = (0, 1, 0)

            # Second traffic ligth
            elif bit == 3:
                if binary[bit] == '0':
                    self.red_1 = (0, 0, 0)
                else:
                    self.red_1 = (1, 0, 0)
            elif bit == 4:
                if binary[bit] == '0':
                    self.yellow_1 = (0, 0, 0)
                else:
                    self.yellow_1 = (1, 1, 0)
            elif bit == 5:
                if binary[bit] == '0':
                    self.green_1 = (0, 0, 0)
                else:
                    self.green_1 = (0, 1, 0)


class SevenSegmentDisplay(Widget):
    leftA = ListProperty([.41, .41, .41])
    leftB = ListProperty([.41, .41, .41])
    leftC = ListProperty([.41, .41, .41])
    leftD = ListProperty([.41, .41, .41])
    leftE = ListProperty([.41, .41, .41])
    leftF = ListProperty([.41, .41, .41])
    leftG = ListProperty([.41, .41, .41])

    rightA = ListProperty([.41, .41, .41])
    rightB = ListProperty([.41, .41, .41])
    rightC = ListProperty([.41, .41, .41])
    rightD = ListProperty([.41, .41, .41])
    rightE = ListProperty([.41, .41, .41])
    rightF = ListProperty([.41, .41, .41])
    rightG = ListProperty([.41, .41, .41])

    # Iterates through the binary at the Input location (RAM) to determine which are 1s and which are 0s
    # Then, activate segments accordingly.
    def activate_segments(self, binary):
        control_bit = int(binary[-1])
        for bit in range(len(binary) - 1):
            if control_bit == 0:
                # if control_bit == 1 then activate the seven left segments depending of the bit.
                if bit == 0:
                    if binary[bit] == '0':
                        self.leftA = (.41, .41, .41)
                    else:
                        self.leftA = (1, 0, 0)
                elif bit == 1:
                    if binary[bit] == '0':
                        self.leftB = (.41, .41, .41)
                    else:
                        self.leftB = (1, 0, 0)
                elif bit == 2:
                    if binary[bit] == '0':
                        self.leftC = (.41, .41, .41)
                    else:
                        self.leftC = (1, 0, 0)
                elif bit == 3:
                    if binary[bit] == '0':
                        self.leftD = (.41, .41, .41)
                    else:
                        self.leftD = (1, 0, 0)
                elif bit == 4:
                    if binary[bit] == '0':
                        self.leftE = (.41, .41, .41)
                    else:
                        self.leftE = (1, 0, 0)
                elif bit == 5:
                    if binary[bit] == '0':
                        self.leftF = (.41, .41, .41)
                    else:
                        self.leftF = (1, 0, 0)
                elif bit == 6:
                    if binary[bit] == '0':
                        self.leftG = (.41, .41, .41)
                    else:
                        self.leftG = (1, 0, 0)
            elif control_bit == 1:
                # if control_bit == 1 then activate the seven right segments depending of the bit.
                if bit == 0:
                    if binary[bit] == '0':
                        self.rightA = (.41, .41, .41)
                    else:
                        self.rightA = (1, 0, 0)
                elif bit == 1:
                    if binary[bit] == '0':
                        self.rightB = (.41, .41, .41)
                    else:
                        self.rightB = (1, 0, 0)
                elif bit == 2:
                    if binary[bit] == '0':
                        self.rightC = (.41, .41, .41)
                    else:
                        self.rightC = (1, 0, 0)
                elif bit == 3:
                    if binary[bit] == '0':
                        self.rightD = (.41, .41, .41)
                    else:
                        self.rightD = (1, 0, 0)
                elif bit == 4:
                    if binary[bit] == '0':
                        self.rightE = (.41, .41, .41)
                    else:
                        self.rightE = (1, 0, 0)
                elif bit == 5:
                    if binary[bit] == '0':
                        self.rightF = (.41, .41, .41)
                    else:
                        self.rightF = (1, 0, 0)
                elif bit == 6:
                    if binary[bit] == '0':
                        self.rightG = (.41, .41, .41)
                    else:
                        self.rightG = (1, 0, 0)


class ASCIIGrid(Widget):

    def __init__(self, **kwargs):
        super(ASCIIGrid, self).__init__(**kwargs)


class GUI(NavigationLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.micro_sim = MicroSim()
        self.add_widget(NavDrawer(micro_sim=self.micro_sim))
        self.add_widget(MainWindow(nav_drawer=self,
                                   app=self.app, micro_sim=self.micro_sim))


class SemrefApp(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Teal'

    def build(self):
        return GUI()
