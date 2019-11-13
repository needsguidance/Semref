import sys
from unittest import TestCase

import mock

from microprocessor_simulator import MicroSim
from tests.test_utils import verify_ram_content_helper
from utils import REGISTER, clear_registers


class SimulatorTest(TestCase):
    ram_content = []
    register_content = []

    def test_array_variable_instructions(self):
        instance = MicroSim()
        return_value = '../output/test5.obj' if sys.platform == 'win32' else 'output/test5.obj'
        with mock.patch('builtins.input', return_value=return_value):
            self.ram_content = [
                ('A80E', 0),  # JMPADDR start
                ('0805', 4),
                ('0AFF', 6),
                ('7300', 8),
                ('0104', 14),  # LOAD R1, valor1
                ('0205', 16),  # LOAD R2, arreglo
                ('0B31', 18),  # LOADIM R3, pi
                ('C940', 20),  # GRT R1, R2
                ('B81C', 22),  # JCONDADDR aca
                ('0C0F', 24),  # LOADIM R4, #0F
                ('A81A', 26),  # JMPADDR stay1
                ('0C0A', 28),  # LOADIM R4, #0A
                ('A81E', 30),  # JMPADDR stay2
            ]
            self.register_content = [
                ('r0', '00'),
                ('r1', '08'),
                ('r2', '05'),
                ('r3', '31'),
                ('r4', '0A'),
                ('r5', '00'),
                ('r6', '00'),
                ('r7', '00'),
                ('pc', '01E'),
                ('sp', '000'),
                ('ir', 'A81E'),
                ('cond', '1')
            ]
            verify_ram_content_helper(self, instance)
            self.verify_register_content()

    def test_simple_instructions(self):
        instance = MicroSim()
        if sys.platform == 'win32':
            return_values = [
                '../output/test.obj',
                '../output/test3.obj',
                '../output/test8.obj',
                '../output/test9.obj',
                '../output/test10.obj'
            ]
        else:
            return_values = [
                'output/test.obj',
                'output/test3.obj',
                'output/test8.obj',
                'output/test9.obj',
                'output/test10.obj'
            ]
        with mock.patch('builtins.input', return_value=return_values[0]):
            self.ram_content = [
                ('0506', 0),  # JMPADDR start
                ('0507', 2),
                ('0000', 4),
                ('0102', 6),  # LOAD R1, valor1
                ('0203', 8),  # LOAD R2, valor2
                ('C940', 10),  # GRT  R1, R2
                ('A812', 12),  # JMPADDR R1esMayor
                ('1A04', 14),  # STORE R2, mayor
                ('A816', 16),  # JMPADDR fin
                ('1904', 18),  # STORE R1, mayor
                ('0B08', 20),  # LOADIM R3, #8
                ('A816', 22)  # JMPADDR fin
            ]
            self.register_content = [
                ('r0', '00'),
                ('r1', '05'),
                ('r2', '07'),
                ('r3', '08'),
                ('r4', '00'),
                ('r5', '00'),
                ('r6', '00'),
                ('r7', '00'),
                ('pc', '016'),
                ('sp', '000'),
                ('ir', 'A816'),
                ('cond', '0')
            ]
            verify_ram_content_helper(self, instance)
            self.verify_register_content()

        with mock.patch('builtins.input', return_value=return_values[1]):
            instance.is_running = True
            verify_ram_content_helper(self, instance)
            self.verify_register_content()

        with mock.patch('builtins.input', return_value=return_values[2]):
            pass

    def test_invalid_instruction(self):
        instance = MicroSim()
        return_value = '../output/test5.obj' if sys.platform == 'win32' else 'output/test5.obj'
        with mock.patch('builtins.input', return_value=return_value):
            with self.assertRaises(SystemError):
                verify_ram_content_helper(self, instance)

    def verify_register_content(self):
        for register in self.register_content:
            self.assertEqual(register[1], REGISTER[register[0]],
                             f'{register[0].upper()} has an incorrect value')
        clear_registers()
