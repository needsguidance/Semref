from kivy.metrics import dp, sp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from microprocessor_simulator import RAM
from utils import ASCII_TABLE


class ASCIIGrid(GridLayout):
    box_pos_x = dp(300)
    box_pos_y = dp(15)

    def __init__(self, **kwargs):
        self.dpi = kwargs.pop('dpi')
        super().__init__(**kwargs)
        self.labels = [
            Label(text='', color=(0, 0, 0, 1), font_size=sp(30)),
            Label(text='', color=(0, 0, 0, 1), font_size=sp(30)),
            Label(text='', color=(0, 0, 0, 1), font_size=sp(30)),
            Label(text='', color=(0, 0, 0, 1), font_size=sp(30)),
            Label(text='', color=(0, 0, 0, 1), font_size=sp(30)),
            Label(text='', color=(0, 0, 0, 1), font_size=sp(30)),
            Label(text='', color=(0, 0, 0, 1), font_size=sp(30)),
            Label(text='', color=(0, 0, 0, 1), font_size=sp(30))
        ]
        if self.dpi < 192:
            self.size_hint = (0.35, 0.1)
            self.pos_hint = {
                'x': dp(0.297),
                'y': dp(-0.066)
            }
        else:
            self.size_hint = (0.35, 0.1)
            self.pos_hint = {
                'x': dp(0.148),
                'y': dp(-0.033)
            }
        for label in self.labels:
            self.add_widget(label)

    def update_ascii_grid(self):
        i = 0
        while i < len(self.labels):
            self.labels[i].text = chr(int(RAM[ASCII_TABLE["port"] + i], 16))
            i += 1
