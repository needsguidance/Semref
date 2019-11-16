
from kivy.metrics import MetricsBase, dp, sp
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors


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
