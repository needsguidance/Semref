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
                ('0000000000110001', 10),
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
                ('0031', 10),
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
                ('0000000000001010', 6),  # const ten 0A
                ('0000000100000010', 8),  # LOAD R1, valor1
                ('0000001000000011', 10),  # LOAD R2, valor2
                ('1100100101000000', 12),  # GRT  R1, R2
                ('1010100000010110', 14),  # JMPADDR R1esMayor
                ('0001101000000100', 16),  # STORE R2, mayor
                ('1010100000011010', 18),  # JMPADDR fin
                ('0001100100000100', 20),  # STORE R1, mayor
                ('0000101100001000', 22),  # LOADIM R3, #8
                ('1010100000011010', 24)  # JMPADDR fin
            ]
            self.hex_content = [
                ('A80A', 0),  # JMPADDR start
                ('0507', 2),
                ('0000', 4),
                ('000A', 6),  # const ten 0A
                ('0102', 8),  # LOAD R1, valor1
                ('0203', 10),  # LOAD R2, valor2
                ('C940', 12),  # GRT  R1, R2
                ('A816', 14),  # JMPADDR R1esMayor
                ('1A04', 16),  # STORE R2, mayor
                ('A81A', 18),  # JMPADDR fin
                ('1904', 20),  # STORE R1, mayor
                ('0B08', 22),  # LOADIM R3, #8
                ('A81A', 24)  # JMPADDR fin
            ]
            self.verify_ram_content_helper()

        with mock.patch('builtins.input', return_value='input/test3.asm'):
            self.binary_content = [
                ('1010100000001010', 0),  # JMPADDR start
                ('0000010100000000', 2),  # valor1 db 5
                ('0000011100000000', 4),  # valor2 db 7
                ('0000000000000000', 6),  # mayor  db 0
                ('0000000000001010', 8),  # const ten 0A
                ('0000000100000010', 10),  # LOAD R1, valor1
                ('0000001000000100', 12),  # LOAD R2, valor2
                ('1100100101000000', 14),  # GRT  R1, R2
                ('1010100000010110', 16),  # JMPADDR R1esMayor
                ('0001101000000110', 18),  # STORE R2, mayor
                ('1010100000011010', 20),  # JMPADDR fin
                ('0001100100000110', 22),  # STORE R1, mayor
                ('0000101100001000', 24),  # LOADIM R3, 8
                ('1010100000011010', 26)  # JMPADDR fin
            ]
            self.hex_content = [
                ('A80A', 0),  # JMPADDR start
                ('0500', 2),  # valor1 db 5
                ('0700', 4),  # valor2 db 7
                ('0000', 6),  # mayor  db 0
                ('000A', 8),  # const ten 0A
                ('0102', 10),  # LOAD R1, valor1
                ('0204', 12),  # LOAD R2, valor2
                ('C940', 14),  # GRT  R1, R2
                ('A816', 16),  # JMPADDR R1esMayor
                ('1A06', 18),  # STORE R2, mayor
                ('A81A', 20),  # JMPADDR fin
                ('1906', 22),  # STORE R1, mayor
                ('0B08', 24),  # LOADIM R3, 8
                ('A81A', 26)  # JMPADDR fin
            ]
            self.verify_ram_content_helper()

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
