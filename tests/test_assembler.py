import sys
from unittest import TestCase

import mock

from assembler import (Assembler)
from tests.test_utils import verify_ram_content_helper


class AssemblerTestCase(TestCase):
    # List of tuples that contain binary/hexadecimal representation of
    # variables/instructions and memory address of said instruction
    binary_content = []
    hex_content = []

    def test_mutliple_variable_array(self):
        """
        Verifies assembler is able to successfully store array values in memory correctly
        """
        instance = Assembler()
        return_value = '../input/test5.asm' if sys.platform == 'win32' else 'input/test5.asm'
        with mock.patch('builtins.input', return_value=return_value):
            self.binary_content = [
                ('1010100000001110', 0),  # JMPADDR start
                ('0000100000000101', 4),
                ('0000101011111111', 6),
                ('0111001100000000', 8),
                ('0000000100000100', 14),  # LOAD R1, valor1
                ('0000001000000101', 16),  # LOAD R2, arreglo
                ('0000101100110001', 18),  # LOADIM R3, pi
                ('1100100101000000', 20),  # GRT R1, R2
                ('1011100000011100', 22),  # JCONDADDR aca
                ('0000110000001111', 24),  # LOADIM R4, #0F
                ('1010100000011010', 26),  # JMPADDR stay1
                ('0000110000001010', 28),  # LOADIM R4, #0A
                ('1010100000011110', 30),  # JMPADDR stay2
            ]
            self.hex_content = [
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
            verify_ram_content_helper(self, instance)

    def test_simple_assembly_instructions(self):
        """
        Verifies generic assembly instructions are assembled correctly
        """
        instance = Assembler()
        if sys.platform == 'win32':
            return_values = [
                '../input/test.asm',
                '../input/test3.asm',
                '../input/test7.asm',
                '../input/test8.asm',
                '../input/test9.asm',
                '../input/test10.asm'
            ]
        else:
            return_values = [
                'input/test.asm',
                'input/test3.asm',
                'input/test7.asm',
                'input/test8.asm',
                'input/test9.asm',
                'input/test10.asm'
            ]
        with mock.patch('builtins.input', return_value=return_values[0]):
            self.binary_content = [
                ('1010100000000110', 0),  # JMPADDR start
                ('0000010100000111', 2),
                ('0000000000000000', 4),
                ('0000000100000010', 6),  # LOAD R1, valor1
                ('0000001000000011', 8),  # LOAD R2, valor2
                ('1100100101000000', 10),  # GRT  R1, R2
                ('1010100000010010', 12),  # JMPADDR R1esMayor
                ('0001101000000100', 14),  # STORE R2, mayor
                ('1010100000010110', 16),  # JMPADDR fin
                ('0001100100000100', 18),  # STORE R1, mayor
                ('0000101100001000', 20),  # LOADIM R3, #8
                ('1010100000010110', 22)  # JMPADDR fin
            ]
            self.hex_content = [
                ('A806', 0),  # JMPADDR start
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
            verify_ram_content_helper(self, instance)

        with mock.patch('builtins.input', return_value=return_values[1]):
            verify_ram_content_helper(self, instance)

        with mock.patch('builtins.input', return_value=return_values[2]):
            self.binary_content = [
                ('1010100000000110', 0),  # JMPADDR begin
                ('0000000000001010', 2),
                ('0000111100000000', 4),
                ('0000110100001100', 6),  # LOADIM R5, #C
                ('0000011000000100', 8),  # LOAD R6, z
                ('1110011010100000', 10),  # NEQ R6, R5
                ('0000011100000010', 12),  # LOAD R7, x
                ('0100111100000001', 14),  # ADDIM R7, #1
                ('0001111100000010', 16),  # STORE x, R7
                ('1011000000000000', 18),  # JCONDRIN R0
                ('1010100000010100', 20),  # JMPADDR fin
            ]
            self.hex_content = [
                ('A806', 0),  # JMPADDR begin
                ('000A', 2),
                ('0F00', 4),
                ('0D0C', 6),  # LOADIM R5, #C
                ('0604', 8),  # LOAD R6, z
                ('E6A0', 10),  # NEQ R6, R5
                ('0702', 12),  # LOAD R7, x
                ('4F01', 14),  # ADDIM R7, #1
                ('1F02', 16),  # STORE x, R7
                ('B000', 18),  # JCONDRIN R0
                ('A814', 20),  # JMPADDR fin
            ]
            verify_ram_content_helper(self, instance)

        with mock.patch('builtins.input', return_value=return_values[3]):
            self.binary_content = [
                ('0000100100000101', 0),  # LOADIM R1, #5
                ('0000101000000010', 2),  # LOADIM R2, #2
                ('0000101100000001', 4),  # LOADIM R3, #1
                ('0010000100000000', 6),  # PUSH R1
                ('1000110001001100', 8),  # SHIFTL R4, R2, R3
                ('1100000100001010', 10),  # LOOP R1, 0A
                ('0001000100000000', 12),  # POP R1
                ('0010110100100000', 14),  # LOADRIND R5, R1
                ('0011000111000000', 16),  # STORERIND R1, R6
                ('1010100000010010', 18),  # JMPADDR fin
            ]
            self.hex_content = [
                ('0905', 0),  # LOADIM R1, #5
                ('0A02', 2),  # LOADIM R2, #2
                ('0B01', 4),  # LOADIM R3, #1
                ('2100', 6),  # PUSH R1
                ('8C4C', 8),  # SHIFTL R4, R2, R3
                ('C10A', 10),  # LOOP R1, 0A
                ('1100', 12),  # POP R1
                ('2D20', 14),  # LOADRIND R5, R1
                ('31C0', 16),  # STORERIND R1, R6
                ('A812', 18),  # JMPADDR fin
            ]
            verify_ram_content_helper(self, instance)

        with mock.patch('builtins.input', return_value=return_values[4]):
            self.binary_content = [
                ('0000100101100100', 0),  # LOADIM R1, #64
                ('0000101000110010', 2),  # LOADIM R2, #32
                ('0000101100000001', 4),  # LOADIM R3, #01
                ('0000110000010000', 6),  # LOADIM R4, #10
                ('0101000100110010', 8),  # SUBIM R1, #32
                ('0110001100101000', 10),  # OR R3, R1, R2
                ('1000010000101100', 12),  # SHIFTR R4, R1, R3
                ('1101100101000000', 14),  # EQ R1, R2
                ('1010010000000000', 16),  # JMPRIND R4
            ]
            self.hex_content = [
                ('0964', 0),  # LOADIM R1, #64
                ('0A32', 2),  # LOADIM R2, #32
                ('0B01', 4),  # LOADIM R3, #01
                ('0C10', 6),  # LOADIM R4, #10
                ('5132', 8),  # SUBIM R1, #32
                ('6328', 10),  # OR R3, R1, R2
                ('842C', 12),  # SHIFTR R4, R1, R3
                ('D940', 14),  # EQ R1, R2
                ('A400', 16),  # JMPRIND R4
            ]
            verify_ram_content_helper(self, instance)

        with mock.patch('builtins.input', return_value=return_values[5]):
            self.binary_content = [
                ('1110100000000000', 14),  # NOP
                ('0000100100000101', 16),  # LOADIM R1, #5
                ('0000110110101100', 18),  # LOADIM R5, #AC
                ('0000111001111001', 20),  # LOADIM R6, #79
                ('1001001110100100', 22),  # ROTAR R3, R5, R1
                ('1001110011000100', 24),  # ROTAL R4, R6, R1
                ('1101001110000000', 26),  # GRTEQ R3, R4
                ('1010100000011110', 28),  # JMPADDR greater
                ('0110100101110000', 30),  # XOR R1, R3, R4
                ('0111001101100000', 32),  # NOT R3, R3
                ('0111110010000000', 34),  # NEG R4, R4
                ('1010100000100100', 36),  # JMPADDR fin
            ]
            self.hex_content = [
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
            verify_ram_content_helper(self, instance)
            self.binary_content.clear()
            self.hex_content.clear()

    def test_subroutine(self):
        """
        Verifies subroutine calls are assembled correctly
        """
        instance = Assembler()
        return_value = '../input/test11.asm' if sys.platform == 'win32' else 'input/test11.asm'
        with mock.patch('builtins.input', return_value=return_value):
            self.binary_content = [
                ('1010100000000010', 0),  # JMPADDR start
                ('0000100100000101', 2),  # LOADIM R1, #5
                ('0000101100000010', 4),  # LOADIM R3, #2
                ('0000110100001010', 6),  # LOADIM R5, #0A
                ('1111000000001100', 8),  # call multiply_by_four
                ('1010010100000000', 10),  # JMPRIND R5
                ('1000101000101100', 12),  # SHIFTL R2, R1, R3
                ('1111100000000000', 14),  # RETURN
            ]
            self.hex_content = [
                ('A802', 0),  # JMPADDR start
                ('0905', 2),  # LOADIM R1, #5
                ('0B02', 4),  # LOADIM R3, #2
                ('0D0A', 6),  # LOADIM R5, #0A
                ('F00C', 8),  # call multiply_by_four
                ('A500', 10),  # JMPRIND R5
                ('8A2C', 12),  # SHIFTL R2, R1, R3
                ('F800', 14),  # RETURN
            ]
            verify_ram_content_helper(self, instance)
            self.binary_content.clear()
            self.hex_content.clear()

    def test_invalid_instruction(self):
        """
         Verifies assembly detects invalid code and raises an error
        """
        if sys.platform == 'win32':
            return_values = [
                '../input/test1.asm',
                '../input/test2.asm',
                '../input/test4.asm',
                '../input/test6.asm'
            ]
        else:
            return_values = [
                'input/test1.asm',
                'input/test2.asm',
                'input/test4.asm',
                'input/test6.asm'
            ]
        with mock.patch('builtins.input', return_value=return_values[0]):
            filename = input()
            asm = Assembler(filename=filename)
            with self.assertRaises(AssertionError):
                asm.read_source()

        with mock.patch('builtins.input', return_value=return_values[1]):
            filename = input()
            asm = Assembler(filename=filename)
            asm.read_source()
            with self.assertRaises(SyntaxError):
                asm.store_instructions_in_ram()

        with mock.patch('builtins.input', return_value=return_values[2]):
            filename = input()
            asm = Assembler(filename=filename)
            asm.read_source()
            with self.assertRaises(MemoryError):
                asm.store_instructions_in_ram()

        with mock.patch('builtins.input', return_value=return_values[3]):
            filename = input()
            asm = Assembler(filename=filename)
            with self.assertRaises(AssertionError):
                asm.read_source()

    def test_invalid_indentation(self):
        """
        Verifies assembler detects indentation errors and raises an error
        """
        if sys.platform == 'win32':
            return_values = [
                '../input/indent_test1.asm',
                '../input/indent_test2.asm',
                '../input/indent_test3.asm',
                '../input/indent_test4.asm',
                '../input/indent_test5.asm',
                '../input/indent_test6.asm',
                '../input/test3.asm'
            ]
        else:
            return_values = [
                'input/indent_test1.asm',
                'input/indent_test2.asm',
                'input/indent_test3.asm',
                'input/indent_test4.asm',
                'input/indent_test5.asm',
                'input/indent_test6.asm',
                'input/test3.asm'
            ]
        with mock.patch('builtins.input', return_value=return_values[0]):
            filename = input()
            asm = Assembler(filename=filename)
            with self.assertRaises(AssertionError):
                asm.read_source()

        with mock.patch('builtins.input', return_value=return_values[1]):
            filename = input()
            asm = Assembler(filename=filename)
            with self.assertRaises(AssertionError):
                asm.read_source()

        with mock.patch('builtins.input', return_value=return_values[2]):
            filename = input()
            asm = Assembler(filename=filename)
            with self.assertRaises(AssertionError):
                asm.read_source()

        with mock.patch('builtins.input', return_value=return_values[3]):
            filename = input()
            asm = Assembler(filename=filename)
            with self.assertRaises(AssertionError):
                asm.read_source()

        with mock.patch('builtins.input', return_value=return_values[4]):
            filename = input()
            asm = Assembler(filename=filename)
            with self.assertRaises(AssertionError):
                asm.read_source()

        with mock.patch('builtins.input', return_value=return_values[5]):
            filename = input()
            asm = Assembler(filename=filename)
            with self.assertRaises(AssertionError):
                asm.read_source()

        with mock.patch('builtins.input', return_value=return_values[6]):
            filename = input()
            asm = Assembler(filename=filename)
            asm.read_source
