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
                '../output/test10.obj'
            ]
        else:
            return_values = [
                'output/test.obj',
                'output/test3.obj',
                'output/test8.obj',
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
            instance.is_running = True
            self.ram_content = [
                ('0905', 0),  # LOADIM R1, #5
                ('0A02', 2),  # LOADIM R2, #2
                ('0B00', 4),  # LOADIM R3, #1
                ('2100', 6),  # PUSH R1
                ('8C4C', 8),  # SHIFTL R4, R2, R3
                ('C10A', 10),  # LOOP R1, 0A
                ('1100', 12),  # POP R1
                ('2D20', 14),  # LOADRIND R5, R1
                ('31C0', 16),  # STORERIND R1, R6
                ('A812', 18),  # JMPADDR fin
                ('0005', 4094)
            ]
            self.register_content = [
                ('r0', '00'),
                ('r1', '05'),
                ('r2', '02'),
                ('r3', '01'),
                ('r4', '04'),
                ('r5', '01'),
                ('r6', '00'),
                ('r7', '00'),
                ('pc', '012'),
                ('sp', '000'),
                ('ir', 'A812'),
                ('cond', '0')
            ]
            verify_ram_content_helper(self, instance)
            self.verify_register_content()

        with mock.patch('builtins.input', return_value=return_values[3]):
            instance.is_running = True
            self.ram_content = [
                ('E800', 14),  # NOP
                ('0905', 16),  # LOADIM R1, #5
                ('0DAC', 18),  # LOADIM R5, #AC
                ('0E79', 20),  # LOADIM R6, #79
                ('93A4', 22),  # ROTAR R3, R5, R1
                ('9CC4', 24),  # ROTAL R4, R6, R1
                ('D380', 26),  # GRTEQ R3, R4
                ('A81E', 28),  # JCONDRIN greater
                ('6970', 30),  # XOR R1, R3, R4
                ('7360', 32),  # NOT R3, R3
                ('7C80', 34),  # NEG R4, R4
                ('A824', 36),  # JMPADDR fin
            ]
            self.register_content = [
                ('r0', '00'),
                ('r1', '1E'),
                ('r2', '00'),
                ('r3', 'F0'),
                ('r4', 'DF'),
                ('r5', 'AC'),
                ('r6', '79'),
                ('r7', '00'),
                ('pc', '024'),
                ('sp', '000'),
                ('ir', 'A824'),
                ('cond', '0')
            ]
            verify_ram_content_helper(self, instance)
            self.verify_register_content()

    def test_invalid_instruction(self):
        instance = MicroSim()
        if sys.platform == 'win32':
            return_values = [
                '../output/test7.obj',
                '../output/test9.obj'
            ]
        else:
            return_values = [
                'output/test7.obj',
                'output/test9.obj'
            ]
        with mock.patch('builtins.input', return_value=return_values[0]):
            with self.assertRaises(SystemError):
                verify_ram_content_helper(self, instance)
            clear_registers()

        with mock.patch('builtins.input', return_value=return_values[1]):
            with self.assertRaises(TimeoutError):
                verify_ram_content_helper(self, instance)
            clear_registers()

    def test_subroutine_instructions(self):
        instance = MicroSim()
        return_value = '../output/test11.obj' if sys.platform == 'win32' else 'output/test11.obj'
        with mock.patch('builtins.input', return_value=return_value):
            self.ram_content = [
                ('A802', 0),  # JMPADDR start
                ('0905', 2),  # LOADIM R1, #5
                ('0B02', 4),  # LOADIM R3, #2
                ('0D0A', 6),  # LOADIM R5, #0A
                ('F00C', 8),  # call multiply_by_four
                ('A500', 10),  # JMPRIND R5
                ('8A2C', 12),  # SHIFTL R2, R1, R3
                ('F800', 14),  # RETURN
            ]
            self.register_content = [
                ('r0', '00'),
                ('r1', '05'),
                ('r2', '14'),
                ('r3', '02'),
                ('r4', '00'),
                ('r5', '0A'),
                ('r6', '00'),
                ('r7', '00'),
                ('pc', '00A'),
                ('sp', '000'),
                ('ir', 'A500'),
                ('cond', '0')
            ]
            verify_ram_content_helper(self, instance)
            self.verify_register_content()

    def verify_register_content(self):
        for register in self.register_content:
            self.assertEqual(register[1], REGISTER[register[0]],
                             f'{register[0].upper()} has an incorrect value')
        clear_registers()
