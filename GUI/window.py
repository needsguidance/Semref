
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivymd.theming import ThemeManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget

from kivymd.uix.filemanager import MDFileManager

from kivymd.uix.navigationdrawer import NavigationDrawerIconButton
from kivymd.toast import toast
from kivy.config import Config
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '650')
Config.set('graphics', 'resizable', False)

# Window tables with editable data rows
# Uses test.kv as a config file

test_kv = """


<ContentNavigationDrawer@MDNavigationDrawer>:
    drawer_logo: 'images/logo.jpg'
    NavigationDrawerSubheader:
        text: "Menu:"
NavigationLayout:
    id: nav_layout
    ContentNavigationDrawer:
        id: nav_drawer
    BoxLayout:
        orientation: 'vertical'
        
        MDToolbar:
            id: toolbar
            title: 'Semref Micro Sim'
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            elevation: 10
            left_action_items:
                [['dots-vertical', lambda x: app.root.toggle_nav_drawer()]]
        GridLayout:
            cols: 2
            row_force_default: True
            row_default_height: 30

            Button:
                text: 'Hello 1'
                size_hint_x: None
                width: 100
            Button:
                text: 'World 1'
                size_hint_x: None
                width: 100
                
            Button:
                text: 'Hello 2'
                size_hint_x: None
                width: 100
            Button:
                text: 'World 2'
                size_hint_x: None
                width: 100

            Button:
                text: 'Hello 3'
                size_hint_x: None
                width: 100
            Button:
                text: 'World 3'
                size_hint_x: None
                width: 100
            Button:
                text: 'Hello 4'
                size_hint_x: None
                width: 100
            Button:
                text: 'World 4'
                size_hint_x: None
                width: 100
            Button:
                text: 'Hello 5'
                size_hint_x: None
                width: 100
            Button:
                text: 'World 5'
                size_hint_x: None
                width: 100

        GridLayout:
            cols: 2
            row_force_default: True
            row_default_height: 30
            pos_hint:{'x': .75}
            Button:
                text: 'Hello 1'
                size_hint_x: None
                width: 100
            Button:
                text: 'World 1'
                size_hint_x: None
                width: 100
                
            Button:
                text: 'Hello 2'
                size_hint_x: None
                width: 100
            Button:
                text: 'World 2'
                size_hint_x: None
                width: 100

            Button:
                text: 'Hello 3'
                size_hint_x: None
                width: 100
            Button:
                text: 'World 3'
                size_hint_x: None
                width: 100
            Button:
                text: 'Hello 4'
                size_hint_x: None
                width: 100
            Button:
                text: 'World 4'
                size_hint_x: None
                width: 100
            Button:
                text: 'Hello 5'
                size_hint_x: None
                width: 100
            Button:
                text: 'World 5'
                size_hint_x: None
                width: 100
        
            
                    

"""



class TestApp(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Teal'


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.manager = None

    def build(self):
        self.main_widget = Builder.load_string(test_kv)
  
        return self.main_widget


    def callback(self, instance, value):
        toast("Pressed item menu %d" % value)

    def on_start(self):
        self.main_widget.ids.nav_drawer.add_widget(
            NavigationDrawerIconButton(icon='checkbox-blank-circle', text='Load File', on_release=self.file_manager_open))
        # for i in range(15):
        #     self.main_widget.ids.nav_drawer.add_widget(
        #         NavigationDrawerIconButton(
        #             icon='checkbox-blank-circle',
        #             text="Item menu %d" % i,
        #             on_release=lambda x, y=i: self.callback(x, y)))

    def file_manager_open(self):
        if not self.manager:
            self.manager = ModalView(size_hint=(1, 1), auto_dismiss=False)
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager, select_path=self.select_path)
            self.manager.add_widget(self.file_manager)
            self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True
        self.manager.open()

    def select_path(self, path):
        """It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;

        """

        self.exit_manager()
        toast(path)

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

 
    