import mock
import sys
from unittest import TestCase

from microprocessor_simulator import RAM, MicroSim
from tests.test_utils import assert_ram_content, verify_ram_content_helper

class SimulatorTest(TestCase):
    ram_content = []

    def test_array_variable_instructions(self):
        micro_sim = MicroSim()
        return_value = '../output/test5.obj' if sys.platform == 'win32' else 'output/test5.obj'
        with mock.patch('builtins.input', return_value=return_value):
            file = input()
            micro_sim.read_obj_file(file)
            micro_sim.run_micro_instructions()
            print(input())