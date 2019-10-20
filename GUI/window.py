from pathlib import Path
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

from microprocessor_simulator import MicroSim

Builder.load_string('''
<Table1>:
    id: data_list
    pos_hint:{'x': 0, 'center_y': .5}
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
    pos_hint:{'x': 0.8, 'center_y': .5}
    RecycleGridLayout:
        cols: 2
        default_size: None, dp(30)
        default_size_hint: 1, None
        size_hint_y: None
        size_hint_x: 0.2
        height: self.minimum_height
        orientation: 'vertical'


''')

class MainWindow(BoxLayout):

    def __init__(self, nav_drawer, **kwargs):
        super().__init__(**kwargs)
        
        self.ids['left_actions'] = BoxLayout()
        self.orientation = 'vertical'
        self.app = App.get_running_app()
        self.add_widget(MDToolbar(title='Semref Micro Sim',
                                  md_bg_color=self.app.theme_cls.primary_color,
                                  background_palette='Primary',
                                  background_hue='500',
                                  elevation=10,
                                  ids=self.ids,
                                  left_action_items=[['dots-vertical', lambda x: nav_drawer.toggle_nav_drawer()]]))
        fl = FloatLayout()
        table1 = Table1()
        table2 = Table2()
        fl.add_widget(table1)
        fl.add_widget(table2)
        self.add_widget(fl)

        self.add_widget(BoxLayout())  # Bumps up navigation bar to the top
        


class NavDrawer(MDNavigationDrawer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drawer_logo = 'images/logo.jpg'
        self.manager_open = False
        self.manager = None
        self.micro_sim = MicroSim()

        self.add_widget(NavigationDrawerSubheader(text='Menu:'))
        self.add_widget(NavigationDrawerIconButton(icon='checkbox-blank-circle',
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
        table.get_data(self.micro_sim.micro_instructions)
        # print(self.micro_sim.micro_instructions)

class Table1(RecycleView):

    def __init__(self, **kwargs):
        super(Table1, self).__init__(**kwargs)        
        self.viewclass = 'Label'
        test = [['hey','heyo'],['hey2','heyo2']]
        self.data = [{"text": str(x),"color": (.1,.1,.1,1)} for row in test for x in row]
        print(self.data)

    def get_data(self, data):
        self.data = [{"text": x,"color": (.1,.1,.1,1)} for x in data]
        print(self.data)
        
class Table2(RecycleView):

    def __init__(self, **kwargs):
        super(Table2, self).__init__(**kwargs)        
        self.viewclass = 'Label'
        test = [['hey3','heyo3'],['hey4','heyo4']]
        self.data = [{"text": str(x),"color": (.1,.1,.1,1)} for row in test for x in row]
        print(self.data)

    def get_data(self, data):
        self.data = [{"text": x,"color": (.1,.1,.1,1)} for x in data]
        print(self.data)
        



class GUI(NavigationLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nav_drawer = NavDrawer()
        self.add_widget(self.nav_drawer)
        self.add_widget(MainWindow(self))


class TestApp(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Teal'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return GUI()
