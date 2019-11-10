from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory

from kivymd.theming import ThemeManager
from kivymd.toast import toast

Builder.load_string('''
# Here a compulsory import
#:import MDDropdownMenu kivymd.uix.menu.MDDropdownMenu


<Menu@Screen>

    MDRaisedButton:
        size_hint: None, None
        size: 3 * dp(48), dp(48)
        text: 'Open menu'
        opposite_colors: True
        pos_hint: {'center_x': .2, 'center_y': .9}
        on_release: MDDropdownMenu(items=app.menu_items, width_mult=3).open(self)

    MDRaisedButton:
        size_hint: None, None
        size: 3 * dp(48), dp(48)
        text: 'Open menu'
        opposite_colors: True
        pos_hint: {'center_x': .2, 'center_y': .1}
        on_release:
            MDDropdownMenu(items=app.menu_items, width_mult=3).open(self)

    MDRaisedButton:
        size_hint: None, None
        size: 3 * dp(48), dp(48)
        text: 'Open menu'
        opposite_colors: True
        pos_hint: {'center_x': .8, 'center_y': .1}
        on_release: MDDropdownMenu(items=app.menu_items, width_mult=3).open(self)

    MDRaisedButton:
        size_hint: None, None
        size: 3 * dp(48), dp(48)
        text: 'Open menu'
        opposite_colors: True
        pos_hint: {'center_x': .8, 'center_y': .9}
        on_release: MDDropdownMenu(items=app.menu_items, width_mult=3).open(self)

    MDRaisedButton:
        size_hint: None, None
        size: 3 * dp(48), dp(48)
        text: 'Open menu'
        opposite_colors: True
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: MDDropdownMenu(items=app.menu_items, width_mult=4).open(self)
''')


class Test(App):
    theme_cls = ThemeManager()
    menu_items = []

    def callback_for_menu_items(self, *args):
        toast(args[0])

    def build(self):
        self.menu_items = [
            {
                "viewclass": "MDMenuItem",
                "text": "Example item %d" % i,
                "callback": self.callback_for_menu_items,
            }
            for i in range(15)
        ]
        return Factory.Menu()


Test().run()