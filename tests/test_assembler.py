from unittest import TestCase

import mock

from assembler import (RAM, Assembler, clear_ram, hexify_ram_content,
                       verify_ram_content)


class AssemblerTestCase(TestCase):

    def test_ram_binary_content(self):
        with mock.patch('builtins.input', return_value='input/test.asm'):
            binary_content = [
                '1010100000001010',  # JMPADDR start
                '0000010100000000',  # valor1 db 5
                '0000011100000000',  # valor2 db 7
                '0000000000000000',  # mayor  db 0
                '0000000000001010',  # const ten 0A
                '0000000100000010',  # LOAD R1, valor1
                '0000001000000100',  # LOAD R2, valor2
                '1100100101000000',  # GRT  R1, R2
                '1010100000010110',  # JMPADDR R1esMayor
                '0001101000000110',  # STORE R2, mayor
                '1010100000011010',  # JMPADDR fin
                '0001100100000110',  # STORE R1, mayor
                '0000101100001000',  # LOADIM R3, 8
                '1010100000011010'  # JMPADDR fin
            ]
            hex_content = [
                'A80A',  # JMPADDR start
                '0500',  # valor1 db 5
                '0700',  # valor2 db 7
                '0000',  # mayor  db 0
                '000A',  # const ten 0A
                '0102',  # LOAD R1, valor1
                '0204',  # LOAD R2, valor2
                'C940',  # GRT  R1, R2
                'A816',  # JMPADDR R1esMayor
                '1A06',  # STORE R2, mayor
                'A81A',  # JMPADDR fin
                '1906',  # STORE R1, mayor
                '0B08',  # LOADIM R3, 8
                'A81A'  # JMPADDR fin
            ]
            self._test_ram_binary_content_helper(
                start=0, binary_content=binary_content, hex_content=hex_content)

        with mock.patch('builtins.input', return_value='input/test3.asm'):
            binary_content = [
                '1010100000001010',  # JMPADDR start
                '0000010100000000',  # valor1 db 5
                '0000011100000000',  # valor2 db 7
                '0000000000000000',  # mayor  db 0
                '0000000000001010',  # const ten 0A
                '0000000100000010',  # LOAD R1, valor1
                '0000001000000100',  # LOAD R2, valor2
                '1100100101000000',  # GRT  R1, R2
                '1010100000010110',  # JMPADDR R1esMayor
                '0001101000000110',  # STORE R2, mayor
                '1010100000011010',  # JMPADDR fin
                '0001100100000110',  # STORE R1, mayor
                '0000101100001000',  # LOADIM R3, 8
                '1010100000011010'  # JMPADDR fin
            ]
            hex_content = [
                'A80A',  # JMPADDR start
                '0500',  # valor1 db 5
                '0700',  # valor2 db 7
                '0000',  # mayor  db 0
                '000A',  # const ten 0A
                '0102',  # LOAD R1, valor1
                '0204',  # LOAD R2, valor2
                'C940',  # GRT  R1, R2
                'A816',  # JMPADDR R1esMayor
                '1A06',  # STORE R2, mayor
                'A81A',  # JMPADDR fin
                '1906',  # STORE R1, mayor
                '0B08',  # LOADIM R3, 8
                'A81A'  # JMPADDR fin
            ]
            self._test_ram_binary_content_helper(
                0, binary_content, hex_content)

            with mock.patch('builtins.input', return_value='input/test3.asm'):
                binary_content = [
                    ('1010100000001110', 0), # JMPADDR start
                    # Variables Go here
                    ('00000001', 14), # LOAD R1, valor1 ??
                    ('00000010', 16), # LOAD R2, arreglo ??
                    ('00001011', 18), # LOADIM R3, pi ??
                    ('1100100101000000', 20), # GRT R1, R2
                    ('1011100000011100', 22), # JCONDADDR aca
                    ('0000110000001111', 24), # LOADIM R4, #0F
                    ('1010100000011010', 26), # JMPADDR stay1
                    ('0000110000001010', 28), # LOADIM R4, #0A
                    ('1010100000011110', 30), #JMPADDR stay2
                ]

    def assert_ram_content(self, start, content):
        """
        Verifies that actual output is aligned with the expected outputs
        :param start: starts reading RAM from given memory location as an int value
        :param content: binary/hexadecimal content to verify
        """
        for c in content:
            self.assertEqual(RAM[start] + RAM[start + 1],
                             c, f'Verify line # {content.index(c) + 1}')
            start += 2

    def _test_ram_binary_content_helper(self, start, binary_content, hex_content):
        """
        Helper to test different input files and verify expected outputs vs actual outputs
        :param start: starts reading from RAM at the given memory location as an int value
        :param binary_content: list of binary values to check
        :param hex_content: list of hex values to check
        """
        clear_ram()
        file = input()
        asm = Assembler(file)
        asm.read_source()
        asm.store_instructions_in_ram()
        verify_ram_content()
        self.assert_ram_content(start, binary_content)

        hexify_ram_content()
        self.assert_ram_content(start, hex_content)
