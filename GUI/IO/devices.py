from queue import Queue
from threading import Condition, Lock, Semaphore, Thread
from time import sleep

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Rectangle
from kivy.metrics import dp, sp
from kivy.properties import ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
from kivymd.uix.button import MDFlatButton

from microprocessor_simulator import RAM
from utils import (ASCII_TABLE, EVENTS, HEX_KEYBOARD, convert_to_hex,
                   hex_to_binary)


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


class HexKeyboard(GridLayout):
    """Keyboard that has hexadecimal system of input in numeric pad"""

    def __init__(self, **kwargs):
        self.mem_table = kwargs.pop('mem_table')
        self.dpi = kwargs.pop('dpi')
        super(HexKeyboard, self).__init__(**kwargs)
        self.queue = Queue(maxsize=10)
        self.lock = Lock()
        self.semaphore = Semaphore()
        self.condition = Condition()
        if self.dpi < 192:
            self.size_hint = (dp(0.4), dp(0.4))
            self.pos_hint = {
                'x': dp(0.10),
                'y': dp(0.35)
            }
        else:
            self.size_hint = (dp(0.4), dp(0.2))
            self.pos_hint = {
                'x': dp(0.105),
                'y': dp(0.1232)
            }

        with self.canvas.before:
            Color(.50, .50, .50, 1)
            Rectangle(pos=(dp(336), dp(249)), size=(dp(362), dp(208)))

        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=(dp(340), dp(254)), size=(dp(354), dp(199)))

            Color(.75, .75, .75, 1)
            Rectangle(pos=(dp(340), dp(250)), size=(dp(353), dp(143)))

            Color(.50, .50, .50, 1)
            for i in range(16):
                if i < 4:
                    Line(rectangle=(dp(340 + (89 * (i % 4))),
                                    dp(357),
                                    dp(87),
                                    dp(35)),
                         width=dp(0.8))
                elif i < 8:
                    Line(rectangle=(dp(340 + (89 * (i % 4))),
                                    dp(322),
                                    dp(87),
                                    dp(35)),
                         width=dp(0.8))
                elif i < 12:
                    Line(rectangle=(dp(340 + (89 * (i % 4))),
                                    dp(287),
                                    dp(87),
                                    dp(35)),
                         width=dp(0.8))
                else:
                    Line(rectangle=(dp(340 + (89 * (i % 4))),
                                    dp(252),
                                    dp(87),
                                    dp(35)),
                         width=dp(0.8))

        for i in range(16):
            if i > 9:
                i = str(chr(i + 55))
            self.add_widget(MDFlatButton(
                text=f'{i}', on_release=self.hex_key_press))

    def hex_key_press(self, instance):
        """
        On hex keyboard press, a thread verifies if RAM is ready to be written.
        Uses a shared queue to enqueue pressed keys that are to be written to RAM.
        :param instance: obj
        """
        thread = Thread(target=self.is_ram_ready)
        if not self.queue.full():
            self.queue.put(hex_to_binary(instance.text))
            thread.start()

    def is_ram_ready(self):
        """
        Utilizes semaphores and monitors to prevent threads from writing to RAM at the same time.
        Current thread is allowed to write to RAM if the LSB is 0, otherwise it must wait.
        """
        with self.semaphore:
            binary = hex_to_binary(RAM[HEX_KEYBOARD['port']])
            if binary[-1] != 0:
                self.condition.acquire()
            self.write_ram()

    def write_ram(self):
        """
        Writes hex keyboard input to RAM.
        Hex input is queued until RAM is ready to receive data
        """
        with self.lock:
            RAM[HEX_KEYBOARD['port']] = convert_to_hex(
                int(f'{self.queue.get()}0001', 2), 8)

            self.mem_table.data_list.clear()
            self.mem_table.get_data()
            sleep(1)
            self.condition.release()
        EVENTS['IS_RAM_EMPTY'] = False


class SevenSegmentDisplay(Widget):
    """Consists of seven LEDs (hence its name) arranged in a rectangular fashion"""
    left_display = ListProperty([
        [.41, .41, .41],
        [.41, .41, .41],
        [.41, .41, .41],
        [.41, .41, .41],
        [.41, .41, .41],
        [.41, .41, .41],
        [.41, .41, .41]
    ])
    right_display = ListProperty([
        [.41, .41, .41],
        [.41, .41, .41],
        [.41, .41, .41],
        [.41, .41, .41],
        [.41, .41, .41],
        [.41, .41, .41],
        [.41, .41, .41]
    ])
    border_color = ListProperty([0, 0, 0, 1])

    # For change the position of the SevenSegment display we need only need change this initials values.
    # Changing this attributes not change the size of the widget.
    box_pos_x = dp(25)
    box_pos_y = dp(100)

    def __init__(self, **kwargs):
        super(SevenSegmentDisplay, self).__init__(**kwargs)
        self.border_color = get_color_from_hex(colors["Blue"]["500"])

    def activate_segments(self, binary):
        """
        Iterates through the binary at the Input location (RAM) to determine which are 1s and which are 0s.
        Then, activate segments accordingly.
        :param binary: str
        """
        control_bit = int(binary[-1])
        if control_bit == 0:
            for i in range(len(self.left_display)):
                if binary[i] == '0':
                    self.left_display[i] = (.41, .41, .41)
                else:
                    self.left_display[i] = (1, 0, 0)
        else:
            for i in range(len(self.right_display)):
                if binary[i] == '0':
                    self.right_display[i] = (.41, .41, .41)
                else:
                    self.right_display[i] = (1, 0, 0)

    def clear_seven_segment(self):
        """
        Resets seven segment display to initial state.
        """
        for i in range(len(self.left_display)):
            self.left_display[i] = (.41, .41, .41)
            self.right_display[i] = (.41, .41, .41)


class TrafficLights(Widget):
    """Set of 3 LED indicators"""
    lights = ListProperty([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    box_pos_x = dp(850)
    box_pos_y = dp(120)

    border_color = ListProperty([0, 0, 0, 1])

    def __init__(self, **kwargs):
        super(TrafficLights, self).__init__(**kwargs)

        # Index of last bits of the byte used as Input for traffic lights
        self.binary = ''  # variable needed for intermittent function
        self.border_color = get_color_from_hex(colors["Blue"]["500"])

    # Scheduler calls method to turn off all lights
    # Parameter dt is the scheduling time
    def intermittent_off(self, dt):
        """
        Turns off LED indicators to simulate intermittent operation
        :param dt: float
        """

        # First traffic light
        if self.binary[-2:] == '11':
            for i in range(len(self.lights)):
                self.lights[i] = (0, 0, 0)

    # Scheduler calls method to turn on all lights
    # Parameter dt is the scheduling time
    def intermittent_on(self, dt):
        """
        Turns on LED indicators to simulate intermittent operation
        :param dt: float
        """
        # First traffic light
        if self.binary[-2:] == '11':
            for i in range(len(self.lights)):
                if i == 0 or i == 3:
                    self.lights[i] = (1, 0, 0)
                elif i == 1 or i == 4:
                    self.lights[i] = (1, 1, 0)
                elif i == 2 or i == 5:
                    self.lights[i] = (0, 1, 0)

    # Iterates through the binary at the Input location (RAM) to determine which are 1s and which are 0s
    # Then, changes colors accordingly.
    def change_color(self, binary):
        """
        Updates LED colors for traffic light. 
        Bits represent the following actions:
            0 -> Turn off LED
            1 -> Turn on LED with predetermined color
        :param binary: str
        """
        self.binary = binary
        for i in range(len(self.lights)):
            if self.binary[i] == '0':
                self.lights[i] = (0, 0, 0)
            elif i == 0 or i == 3:
                self.lights[i] = (1, 0, 0)
            elif i == 1 or i == 4:
                self.lights[i] = (1, 1, 0)
            elif i == 2 or i == 5:
                self.lights[i] = (0, 1, 0)
