from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.metrics import MetricsBase, dp, sp
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors

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
        if control_bit == 1:
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
