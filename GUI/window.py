
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
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.theming import ThemeManager
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.navigationdrawer import NavigationDrawerIconButton
from microprocessor_simulator import MicroSim

# from kivy.config import Config
# Config.set('graphics', 'width', '1024')
# Config.set('graphics', 'height', '650')
# Config.set('graphics', 'resizable', False)

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

        Widget:
"""

class TestApp(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Teal'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Window.bind(on_keyboard=self.events)
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

    def file_manager_open(self, instance):
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
        sim = MicroSim()
        sim.read_obj_file(path)
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
