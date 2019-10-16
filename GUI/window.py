
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivymd.theming import ThemeManager
from kivy.lang import Builder

from kivymd.uix.navigationdrawer import NavigationDrawerIconButton
from kivymd.toast import toast
# from kivy.config import Config
# Config.set('graphics', 'width', '1024')
# Config.set('graphics', 'height', '650')
# Config.set('graphics', 'resizable', False)

# Window tables with editable data rows
#Uses test.kv as a config file

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

class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, Window, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(Window, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, Window, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self):
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):
        self.text = txt
    
    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.popup = Popup(title='Load file', content=content, size_hint=(0.9,0.9))
        self.popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text = stream.read()
            self.popup = TextInputPopup(self)
    
    def dismiss_popup(self):
        self.popup.dismiss()


class Window(BoxLayout):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super(Window, self).__init__(**kwargs)
        self.append_data()

        self.load_button = Button(text='Load File')
        self.add_widget(self.load_button)
        self.left_button = Button(text="Left", pos_hint={'x': .35, 'top': .3}, size_hint=(.1, .1), id='left')

    def append_data(self):
        rows = []
        this = [['this','that'], ['this2', 'that2'],  ['this3', 'that3'],  ['this4', 'that4']]
        rows.append(this)

        # create data_items
        for row in rows:
            for col in row:
                self.data_items.append(col)

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class TestApp(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Teal'

    def build(self):
        self.main_widget = Builder.load_string(test_kv)
        return self.main_widget

    def callback(self, instance, value):
        toast("Pressed item menu %d" % value)

    def on_start(self):
        self.main_widget.ids.nav_drawer.add_widget(
            NavigationDrawerIconButton(icon='checkbox-blank-circle', text='Load File', on_release=lambda x: self.callback(x, 1)))
        # for i in range(15):
        #     self.main_widget.ids.nav_drawer.add_widget(
        #         NavigationDrawerIconButton(
        #             icon='checkbox-blank-circle', 
        #             text="Item menu %d" % i,
        #             on_release=lambda x, y=i: self.callback(x, y)))
    

    # def build(self):
    #     return Window()


