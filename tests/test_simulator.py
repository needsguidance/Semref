from unittest import TestCase

from microprocessor_simulator import RAM, MicroSim
from tests.test_utils import assert_ram_content

class SimulatorTest(TestCase):
    hex_content = []
    pass

    def verify_ram_content_helper(self):
        """
        Helper to test different input files and verify expected outputs vs actual outputs
        """
        RAM = ['00' for i in range(4096)]
        file = input()
        micro_sim = MicroSim()
        micro_sim.read_obj_file(file)
        assert_ram_content(self, self.hex_content)