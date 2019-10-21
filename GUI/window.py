from pathlib import Path
from kivy import Config

Config.set('graphics', 'resizable', False)
from kivymd.uix.button import MDFlatButton, MDRectangleFlatIconButton, MDFillRoundFlatIconButton
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ListProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.theming import ThemeManager
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.navigationdrawer import (MDNavigationDrawer, MDToolbar,
                                         NavigationDrawerIconButton,
                                         NavigationDrawerSubheader,
                                         NavigationLayout)

from microprocessor_simulator import MicroSim, RAM

Builder.load_string('''
<Table1>:
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
        
        
<Table2>:
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
    step_index = 0

    def __init__(self, **kwargs):
        self.app = kwargs.pop('app')
        self.micro_sim = kwargs.pop('micro_sim')
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
        self.refresh_button = MDFillRoundFlatIconButton(text='Refresh',
                                                        icon='refresh',
                                                        size_hint=(None, None),
                                                        pos_hint={'center_x': .5, 'center_y': 2.12},
                                                        on_release=self.refresh)
        self.add_widget(self.run_button)
        self.add_widget(self.debug_button)
        self.add_widget(self.refresh_button)
        table1 = Table1()
        table2 = Table2()
        self.add_widget(table1)
        self.add_widget(table2)

    def run_micro_instructions(self, instance):
        if not self.micro_sim.is_ram_loaded:
            toast('Must load file first before running')
        else:
            self.micro_sim.run_micro_instructions()
            for i in self.micro_sim.micro_instructions:
                if i != 'NOP':
                    print(i)
            # print(self.micro_sim.micro_instructions)
        # toast(self.micro_sim.micro_instructions.__str__())

    def refresh(self, instance):
        toast('Not Implemented HueHue')

    def run_micro_instructions_step(self, instance):
        if not self.micro_sim.is_ram_loaded:
            toast('Must load file first before running')
        else:
            self.micro_sim.run_micro_instructions_step(self.step_index)
            self.step_index +=2
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
    data = ListProperty([])

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
            
        table = Table1()
        i = 0
        for m in range(50):
            self.data.append(f'{RAM[i]} {RAM[i + 1]}')
            i += 2
        
        table.get_data(self.data)
        
        # print(self.micro_sim.micro_instructions)


class Table1(RecycleView):
    data_list = ListProperty([])


    def __init__(self, **kwargs):
        super(Table1, self).__init__(**kwargs)
        self.viewclass = 'Label'
        test = [['hey','heyo'],['hey2','heyo2']]
        for row in test:
            for x in row:
                self.get_data(x)

        # self.data = [{"text": str(x),"color": (.1,.1,.1,1)} for x in range(50)]

        # self.data = [{"text": str(x),"color": (.1,.1,.1,1)} for row in test for x in row]
        print(self.data)

    def get_data(self, data):
        self.data_list.append(data)
        self.data = [{"text": str(x),"color": (.1,.1,.1,1)} for x in self.data_list]
        print(self.data)
        
        
        
class Table2(RecycleView):
    data_list = ListProperty([])

    def __init__(self, **kwargs):
        super(Table2, self).__init__(**kwargs)    
        self.viewclass = 'Label'
        test = [['hey3','heyo3'],['hey4','heyo4']]
        for row in test:
            for x in row:
                self.get_data(x)
        # self.data = [{"text": str(x),"color": (.1,.1,.1,1)} for x in range(50)]

        # self.data = [{"text": str(x),"color": (.1,.1,.1,1)} for row in test for x in row]
        print(self.data)

    def get_data(self, data):
        
        self.data_list.append(data)
        self.data = [{"text": str(x),"color": (.1,.1,.1,1)} for x in self.data_list]
        print(self.data)
        
       

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
