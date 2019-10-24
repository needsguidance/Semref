import secrets
from pathlib import Path

from kivy import Config

from constants import REGISTER

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '650')
Config.set('graphics', 'resizable', False)
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import (ListProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.uix.recycleview import RecycleView
from kivymd.theming import ThemeManager
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.navigationdrawer import (MDNavigationDrawer, MDToolbar,
                                         NavigationDrawerIconButton,
                                         NavigationDrawerSubheader,
                                         NavigationLayout)

from microprocessor_simulator import MicroSim, RAM

Builder.load_string('''
<RegisterTable>:
    id: data_list
    pos_hint:{'x': 0, 'center_y': 1.5}
    RecycleGridLayout:
        canvas.before:
            Color: 
                rgba: .75, .75, .75, 1
            Rectangle:
                pos: self.pos
                size: self.size
        canvas:
            Color:
                rgba: .50, .50, .50, 1
            Line:
                width: 2.
                rectangle: (self.x, self.y, self.width, self.height) 

        cols: 2
        default_size: None, dp(30)
        default_size_hint: 1, None
        size_hint_y: None
        size_hint_x: 0.2
        height: self.minimum_height
        orientation: 'vertical'

<InstructionTable>:
    id: data_list
    pos_hint:{'x': 0.2, 'center_y': 1.5}
    RecycleGridLayout:
        cols: 3
        default_size: None, dp(30)
        default_size_hint: 1, None
        size_hint_y: None
        size_hint_x: 0.5
        height: self.minimum_height
        orientation: 'vertical'
        
        
<MemoryTable>:
    id: data_list
    pos_hint:{'x': 0.75, 'center_y': 1.5}
    RecycleGridLayout:
        canvas.before:
            Color: 
                rgba: .75, .75, .75, 1
            Rectangle:
                pos: self.pos
                size: self.size
        canvas:
            Color:
                rgba: .50, .50, .50, 1
            Line:
                width: 2.
                rectangle: (self.x, self.y, self.width, self.height) 
        cols: 2
        default_size: None, dp(30)
        default_size_hint: 1, None
        size_hint_y: None
        size_hint_x: 0.25
        height: self.minimum_height
        orientation: 'vertical'

<TrafficLights>
    canvas.before:
        Color:
            rgb: 0,0,0
        Rectangle:
            pos: 50, 60
            size: 85, 106
        Color:
            rgb: self.red_1
        Ellipse:
            pos: 100, 130
            size: 25, 25
        Color:
            rgb: self.yellow_1
        Ellipse:
            pos: 100, 100
            size: 25, 25
        Color:
            rgb: self.green_1
        Ellipse:
            pos: 100, 70
            size: 25, 25
        Color:
            rgb: self.red_2
        Ellipse:
            pos: 60, 130
            size: 25, 25
        Color:
            rgb: self.yellow_2
        Ellipse:
            pos: 60, 100
            size: 25, 25
        Color:
            rgb: self.green_2
        Ellipse:
            pos: 60, 70
            size: 25, 25
            
<SevenSegmentDisplay>
    canvas.before:
        Color:
            rgb: 0,0,0
        Rectangle:
            pos: 50, 60
            size: 205, 200
        # A
        Color:
            rgb: self.on_color
        Rectangle:
            pos: 70, 230
            size: 60, 10
        # B   
        Color:
            rgb: self.on_color
        Rectangle:
            pos: 130, 160
            size: 10, 70   
        # C
        Color:
            rgb: self.on_color
        Rectangle:
            pos: 130, 80
            size: 10, 70 
        # D
        Color:
            rgb: self.off_color
        Rectangle:
            pos: 70, 70
            size: 60, 10
        # E
        Color:
            rgb: self.off_color
        Rectangle:
            pos: 60, 80
            size: 10, 70       
        # F
        Color:
            rgb: self.off_color
        Rectangle:
            pos: 60, 160
            size: 10, 70   
            
        # G
        Color:
            rgb: self.off_color
        Rectangle:
            pos: 70, 150
            size: 60, 10
# ############    Right Number ############
        # A
        Color:
            rgb: self.off_color
        Rectangle:
            pos: 175, 230
            size: 60, 10
        # B
        Color:
            rgb: self.off_color
        Rectangle:
            pos: 235, 160
            size: 10, 70   
        # C
        Color:
            rgb: self.off_color
        Rectangle:
            pos: 235, 80
            size: 10, 70   
        # D
        Color:
            rgb: self.off_color
        Rectangle:
            pos: 175, 70
            size: 60, 10
        # E
        Color:
            rgb: self.off_color
        Rectangle:
            pos: 165, 80
            size: 10, 70       
        # F
        Color:
            rgb: self.off_color
        Rectangle:
            pos: 165, 160
            size: 10, 70   
            
        #     G
        Color:
            rgb: self.off_color
        Rectangle:
            pos: 175, 150
            size: 60, 10

''')


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
                                                    pos_hint={'center_x': .7, 'center_y': 2.12},
                                                    on_release=self.run_micro_instructions)
        self.debug_button = MDFillRoundFlatIconButton(text='Debug',
                                                      icon='android-debug-bridge',
                                                      size_hint=(None, None),
                                                      pos_hint={'center_x': .9, 'center_y': 2.12},
                                                      on_release=self.run_micro_instructions_step)
        self.refresh_button = MDFillRoundFlatIconButton(text='Clear',
                                                        icon='refresh',
                                                        size_hint=(None, None),
                                                        pos_hint={'center_x': .5, 'center_y': 2.12},
                                                        on_release=self.clear)
        self.save_button = MDFillRoundFlatIconButton(text='Save File',
                                                     icon='download',
                                                     size_hint=(None, None),
                                                     pos_hint={'center_x': .35, 'center_y': 2.12},
                                                     on_release=self.save)
        self.add_widget(self.save_button)
        self.add_widget(self.run_button)
        self.add_widget(self.debug_button)
        self.add_widget(self.refresh_button)
        self.reg_table = RegisterTable()
        self.mem_table = MemoryTable()
        self.inst_table = InstructionTable()
        self.reg_table.get_data()
        self.mem_table.data_list.clear()
        self.mem_table.get_data()
        self.light = TrafficLights()
        self.seven_segment_display = SevenSegmentDisplay()
        self.inst_table.data_list.clear()
        self.inst_table.get_data(self.micro_sim.index, self.header, self.micro_sim.disassembled_instruction())
        self.header = True
        print(RAM[4085])
        RAM[4085] = '80'
        self.light.change_color(self.micro_sim.traffic_lights_binary())

        self.add_widget(self.reg_table)
        self.add_widget(self.inst_table)
        self.add_widget(self.mem_table)
        # self.add_widget(self.light)
        self.add_widget(self.seven_segment_display)

    def save(self, instance):
        toast("Not Implemented yet. Will be ready on Sprint 3")
        RAM[4085] = secrets.token_hex(1)
        self.light.change_color(self.micro_sim.traffic_lights_binary())

    def run_micro_instructions(self, instance):
        if not self.micro_sim.is_running:
            toast("Infinite loop encountered. Program stopped")
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

                        while self.micro_sim.is_running:
                            self.micro_sim.run_micro_instructions()
                            self.inst_table.get_data(self.micro_sim.index, self.header,
                                                     self.micro_sim.disassembled_instruction())

                            if self.micro_sim.prev_index == self.micro_sim.index:
                                self.micro_sim.is_running = False
                            else:
                                self.micro_sim.prev_index = self.micro_sim.index

                self.reg_table.get_data()
                self.mem_table.data_list.clear()
                self.mem_table.get_data()

                toast('File executed successfully')
                for i in self.micro_sim.micro_instructions:
                    if i != 'NOP':
                        print(i)

    def clear(self, instance):
        self.header = False
        self.step_index = 0
        self.micro_sim.micro_clear()
        self.reg_table.data_list.clear()
        self.reg_table.get_data()
        self.mem_table.data_list.clear()
        self.mem_table.get_data()
        self.inst_table.data_list.clear()
        self.inst_table.get_data(self.micro_sim.index, self.header, self.micro_sim.disassembled_instruction())
        self.header = True
        self.first_inst = True

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

                    self.micro_sim.run_micro_instructions_step(self.step_index)
                    self.reg_table.get_data()
                    self.mem_table.data_list.clear()
                    self.mem_table.get_data()
                    self.inst_table.get_data(self.micro_sim.index, self.header,
                                             self.micro_sim.disassembled_instruction())

                toast('Runnin instruction in step-by-step mode. Step ' + str(self.step_index) + ' is running')
                for i in self.micro_sim.micro_instructions:
                    if i != 'NOP':
                        print(i)


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

        self.add_widget(NavigationDrawerSubheader(text='Menu:'))
        self.add_widget(NavigationDrawerIconButton(icon='paperclip',
                                                   text='Load File',
                                                   on_release=self.file_manager_open))

    def file_manager_open(self, instance):
        if not self.manager:
            self.manager = ModalView(size_hint=(1, 1), auto_dismiss=False)
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
                _data.append({'text': self.data_list[i].upper(), 'color': (177 / 255, 62 / 255, 88 / 255, 1)})
                _data.append({'text': self.data_list[i + 1].upper(), 'color': (177 / 255, 62 / 255, 88 / 255, 1)})
            else:
                _data.append({'text': self.data_list[i].upper(), 'color': (.1, .1, .1, 1)})
                _data.append({'text': self.data_list[i + 1].upper(), 'color': (.1, .1, .1, 1)})
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

        self.data = [{"text": str(x.upper()), "color": (.1, .1, .1, 1)} for x in self.data_list]


class InstructionTable(RecycleView):
    data_list = ListProperty([])

    def __init__(self, **kwargs):
        # self.register = REGISTER
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
        self.data = [{"text": str(x.upper()), "color": (.1, .1, .1, 1)} for x in self.data_list]


class TrafficLights(Widget):
    red_1 = ListProperty([1, 0, 0])
    red_2 = ListProperty([1, 0, 0])
    yellow_1 = ListProperty([1, 1, 0])
    yellow_2 = ListProperty([1, 1, 0])
    green_1 = ListProperty([0, 1, 0])
    green_2 = ListProperty([0, 1, 0])

    def __init__(self, **kwargs):
        super(TrafficLights, self).__init__(**kwargs)

    def change_color(self, binary):
        print(binary)
        for bit in range(len(binary)):
            if bit == 0:
                if binary[bit] == '0':
                    self.red_1 = (0, 0, 0)
                    print(bit)
                else:
                    self.red_1 = (1, 0, 0)
            elif bit == 1:
                if binary[bit] == '0':
                    self.yellow_1 = (0, 0, 0)
                else:
                    self.yellow_1 = (1, 1, 0)
            elif bit == 2:
                if binary[bit] == '0':
                    self.green_1 = (0, 0, 0)
                else:
                    self.green_1 = (0, 1, 0)
            elif bit == 3:
                if binary[bit] == '0':
                    self.red_2 = (0, 0, 0)
                else:
                    self.red_2 = (1, 0, 0)
            elif bit == 4:
                if binary[bit] == '0':
                    self.yellow_2 = (0, 0, 0)
                else:
                    self.yellow_2 = (1, 1, 0)
            elif bit == 5:
                if binary[bit] == '0':
                    self.green_2 = (0, 0, 0)
                else:
                    self.green_2 = (0, 1, 0)


class SevenSegmentDisplay(Widget):
    off_color = ListProperty([.41, .41, .41])
    on_color = ListProperty([1, 0, 0])

    # TODO: Implement logic for display.
    # leftA
    # leftB
    # leftC
    # leftD
    # leftE
    # leftF
    # leftG

    def __init__(self, **kwargs):
        super(SevenSegmentDisplay, self).__init__(**kwargs)


class GUI(NavigationLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.micro_sim = MicroSim()
        self.add_widget(NavDrawer(micro_sim=self.micro_sim))
        self.add_widget(MainWindow(nav_drawer=self, app=self.app, micro_sim=self.micro_sim))


class TestApp(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Teal'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return GUI()
