from pathlib import Path

from kivy import Config

from constants import REGISTER

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '650')
Config.set('graphics', 'resizable', False)
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.app import App
from kivy.lang import Builder
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
<register_table>:
    id: data_list
    pos_hint:{'x': 0, 'center_y': 1.5}
    RecycleGridLayout:
        cols: 2
        default_size: None, dp(30)
        default_size_hint: 1, None
        size_hint_y: None
        size_hint_x: 0.2
        height: self.minimum_height
        orientation: 'vertical'
        
        
<memory_table>:
    id: data_list
    pos_hint:{'x': 0.8, 'center_y': 1.5}
    RecycleGridLayout:
        cols: 2
        default_size: None, dp(30)
        default_size_hint: 1, None
        size_hint_y: None
        size_hint_x: 0.2
        height: self.minimum_height
        orientation: 'vertical'


''')


class RunWindow(FloatLayout):

    def __init__(self, **kwargs):
        self.app = kwargs.pop('app')
        self.micro_sim = kwargs.pop('micro_sim')
        self.step_index = 0
        self.register = kwargs.pop('registers')
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
        self.add_widget(self.run_button)
        self.add_widget(self.debug_button)
        self.add_widget(self.refresh_button)
        self.reg_table = register_table()
        self.mem_table = memory_table()
        self.reg_table.data_list.clear()
        self.reg_table.get_data()
        self.mem_table.data_list.clear()
        self.mem_table.get_data()
        
        self.add_widget(self.reg_table)
        self.add_widget(self.mem_table)

    def run_micro_instructions(self, instance):
        if not(self.micro_sim.is_running):
            toast("Infinite loop encountered. Program stopped")
        else:
            if not self.micro_sim.is_ram_loaded:
                toast('Must load file first before running')
            else:
                self.micro_sim.run_micro_instructions()
                toast('File executed successfully')
                for i in self.micro_sim.micro_instructions:
                    if i != 'NOP':
                        print(i)
        
        self.reg_table.data_list.clear()
        self.reg_table.get_data()
        self.mem_table.data_list.clear()
        self.mem_table.get_data()

    def clear(self, instance):
        self.micro_sim.micro_clear()

        toast('Micro memory cleared! Load new data')

    def run_micro_instructions_step(self, instance):
        if not(self.micro_sim.is_running):
            toast("Infinite loop encountered. Program stopped")
        else:
            if not self.micro_sim.is_ram_loaded:
                toast('Must load file first before running')
            else:
                self.step_index += 1
                self.micro_sim.run_micro_instructions_step(self.step_index)
                toast('Runnin instruction in step-by-step mode. Step ' + str(self.step_index) + ' is running')
                for i in self.micro_sim.micro_instructions:
                    if i != 'NOP':
                        print(i)
        
        self.reg_table.data_list.clear()
        self.reg_table.get_data()
        self.mem_table.data_list.clear()
        self.mem_table.get_data()


class MainWindow(BoxLayout):

    def __init__(self, **kwargs):
        self.nav_drawer = kwargs.pop('nav_drawer')
        self.app = kwargs.pop('app')
        self.micro_sim = kwargs.pop('micro_sim')
        self.register = kwargs.pop('registers')
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
        self.add_widget(RunWindow(app=self.app, micro_sim=self.micro_sim, registers=self.register))


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


class register_table(RecycleView):
    data_list = ListProperty([])

    def __init__(self, **kwargs):
        # self.register = REGISTER
        super(register_table, self).__init__(**kwargs)
        self.viewclass = 'Label'

    def get_data(self):
        for k, v in REGISTER.items():
            self.data_list.append(k)
            self.data_list.append(v)

        self.data = [{"text": str(x.upper()), "color": (.1, .1, .1, 1)} for x in self.data_list]


class memory_table(RecycleView):
    data_list = ListProperty([])

    def __init__(self, **kwargs):
        # self.register = REGISTER
        super(memory_table, self).__init__(**kwargs)
        self.viewclass = 'Label'


    def get_data(self):
        i = 0
        for m in range(50):
            self.data_list.append(f'{RAM[i]}')
            self.data_list.append(f'{RAM[i + 1]}')
            i+= 2
          

        self.data = [{"text": str(x.upper()), "color": (.1, .1, .1, 1)} for x in self.data_list]


class GUI(NavigationLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.micro_sim = MicroSim()
        self.add_widget(NavDrawer(micro_sim=self.micro_sim))
        self.add_widget(MainWindow(nav_drawer=self, app=self.app, micro_sim=self.micro_sim, registers=REGISTER))


class TestApp(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Teal'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return GUI()
