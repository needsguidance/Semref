from queue import Queue
from threading import Lock, Semaphore, Condition, Thread
from time import sleep

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDFlatButton

from microprocessor_simulator import RAM
from utils import hex_to_binary, HEX_KEYBOARD, convert_to_hex, EVENTS


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
            self.add_widget(MDFlatButton(text=f'{i}', on_release=self.hex_key_press))

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
