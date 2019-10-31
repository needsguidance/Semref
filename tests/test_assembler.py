from unittest import TestCase

import mock

from assembler import (RAM, Assembler, clear_ram, hexify_ram_content,
                       verify_ram_content)


class AssemblerTestCase(TestCase):

    # List of tuples that containt binary/hexadecimal representation of
    # variables/instructions and memory address of said instruction
    binary_content = []
    hex_content = []

    def test_mutliple_variable_array(self):
        with mock.patch('builtins.input', return_value='input/test5.asm'):
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
            self.verify_ram_content_helper()

    def test_simple_assembly_instructions(self):
        with mock.patch('builtins.input', return_value='input/test.asm'):
            self.binary_content = [
                ('1010100000001010', 0),  # JMPADDR start
                ('0000010100000111', 2),
                ('0000000000000000', 4),
                ('0000000100000010', 6),  # LOAD R1, valor1
                ('0000001000000011', 8),  # LOAD R2, valor2
                ('1100100101000000', 10),  # GRT  R1, R2
                ('1010100000010110', 12),  # JMPADDR R1esMayor
                ('0001101000000100', 14),  # STORE R2, mayor
                ('1010100000011010', 16),  # JMPADDR fin
                ('0001100100000100', 18),  # STORE R1, mayor
                ('0000101100001000', 20),  # LOADIM R3, #8
                ('1010100000011010', 22)  # JMPADDR fin
            ]
            self.hex_content = [
                ('A80A', 0),  # JMPADDR start
                ('0507', 2),
                ('0000', 4),
                ('0102', 6),  # LOAD R1, valor1
                ('0203', 8),  # LOAD R2, valor2
                ('C940', 10),  # GRT  R1, R2
                ('A816', 12),  # JMPADDR R1esMayor
                ('1A04', 14),  # STORE R2, mayor
                ('A81A', 16),  # JMPADDR fin
                ('1904', 18),  # STORE R1, mayor
                ('0B08', 20),  # LOADIM R3, #8
                ('A81A', 22)  # JMPADDR fin
            ]
            self.verify_ram_content_helper()
        
        with mock.patch('builtins.input', return_value='input/test3.asm'):
            self.binary_content = [
                ('1010100000001010', 0),  # JMPADDR start
                ('0000010100000111', 2),
                ('0000000000000000', 4),
                ('0000000100000010', 6),  # LOAD R1, valor1
                ('0000001000000011', 8),  # LOAD R2, valor2
                ('1100100101000000', 10),  # GRT  R1, R2
                ('1010100000010110', 12),  # JMPADDR R1esMayor
                ('0001101000000100', 14),  # STORE R2, mayor
                ('1010100000011010', 16),  # JMPADDR fin
                ('0001100100000100', 18),  # STORE R1, mayor
                ('0000101100001000', 20),  # LOADIM R3, #8
                ('1010100000011010', 22)  # JMPADDR fin
            ]
            self.hex_content = [
                ('A80A', 0),  # JMPADDR start
                ('0507', 2),
                ('0000', 4),
                ('0102', 6),  # LOAD R1, valor1
                ('0203', 8),  # LOAD R2, valor2
                ('C940', 10),  # GRT  R1, R2
                ('A816', 12),  # JMPADDR R1esMayor
                ('1A04', 14),  # STORE R2, mayor
                ('A81A', 16),  # JMPADDR fin
                ('1904', 18),  # STORE R1, mayor
                ('0B08', 20),  # LOADIM R3, #8
                ('A81A', 22)  # JMPADDR fin
            ]
            self.verify_ram_content_helper()
        
        with mock.patch('builtins.input', return_value='input/test7.asm'):
            self.binary_content = [
                ('1010100000000100', 0), # JMPADDR begin
                ('0000000000001010', 2),
                ('0000111100000000', 4),
                ('0000110100001100', 6), # LOADIM R5, #C
                ('0000011000000100', 8), # LOAD R6, z
                ('1110011010100000', 10), # NEQ R6, R5
                ('0000011100000010', 12), # LOAD R7, x
                ('0100111100000001', 14), # ADDIM R7, #1
                ('0001111100000010', 16), # STORE x, R7
                ('1011000000000000', 18), # JCONDRIN R0
                ('1010100000010100', 20), # JMPADDR fin
            ]
            self.hex_content = [
                ('A804', 0), # JMPADDR begin
                ('000A', 2),
                ('0F00', 4),
                ('0D0C', 6), # LOADIM R5, #C
                ('0604', 8), # LOAD R6, z
                ('E6A0', 10), # NEQ R6, R5
                ('0702', 12), # LOAD R7, x
                ('4F01', 14), # ADDIM R7, #1
                ('1F02', 16), # STORE x, R7
                ('B000', 18), # JCONDRIN R0
                ('A814', 20), # JMPADDR fin
            ]
            self.verify_ram_content_helper()

        with mock.patch('builtins.input', return_value='input/test8.asm'):
            self.binary_content = [

            ]

    def test_invalid_instruction(self):
        with mock.patch('builtins.input', return_value='input/test1.asm'):
            file = input()
            asm = Assembler(file)
            asm.read_source()
            with self.assertRaises(SyntaxError):
                asm.store_instructions_in_ram()
        
        with mock.patch('builtins.input', return_value='input/test2.asm'):
            file = input()
            asm = Assembler(file)
            asm.read_source()
            with self.assertRaises(SyntaxError):
                asm.store_instructions_in_ram()
            
        with mock.patch('builtins.input', return_value='input/test4.asm'):
            file = input()
            asm = Assembler(file)
            asm.read_source()
            with self.assertRaises(MemoryError):
                asm.store_instructions_in_ram()

        with mock.patch('builtins.input', return_value='input/test6.asm'):
            file = input()
            asm = Assembler(file)
            asm.read_source()
            with self.assertRaises(MemoryError):
                asm.store_instructions_in_ram()

    def assert_ram_content(self, content):
        """
        Verifies that actual output is aligned with the expected outputs
        :param start: starts reading RAM from given memory location as an int value
        :param content: binary/hexadecimal content to verify
        """
        for c in content:
            self.assertEqual(RAM[c[1]] + RAM[c[1] + 1],
                             c[0], f'Verify line # {content.index(c) + 1}')

    def verify_ram_content_helper(self):
        """
        Helper to test different input files and verify expected outputs vs actual outputs
        """
        clear_ram()
        file = input()
        asm = Assembler(file)
        asm.read_source()
        asm.store_instructions_in_ram()

        verify_ram_content()
        self.assert_ram_content(self.binary_content)

        hexify_ram_content()
        self.assert_ram_content(self.hex_content)
        self.binary_content.clear()
        self.hex_content.clear()
