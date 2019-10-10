import unittest

import mock

from assembler import Assembler, verify_ram_content, RAM, hexify_ram_content, clear_ram


def yes_or_no():
    answer = input("Do you want to quit? > ")
    if answer == "yes":
        return ("Quitter!")
    elif answer == "no":
        return ("Awesome!")
    else:
        return ("BANG!")


class InputTestCase(unittest.TestCase):

    def test_invalid_input(self):
        with mock.patch('builtins.input', return_value="input.txt"):
            file = input()
            with self.assertRaises(AssertionError):
                Assembler(file)

        with mock.patch('builtins.input', return_value="input/test.asm"):
            file = input()
            asm = Assembler(file)
            with self.assertRaises(FileNotFoundError):
                asm.read_source()

    def test_valid_input(self):
        with mock.patch('builtins.input', return_value="..input/test.asm"):
            file = input()
            asm = Assembler(file)
            self.assertEqual(file, asm.filename, 'Filenames do not match')

    def test_ram_binary_content(self):
        with mock.patch('builtins.input', return_value="../input/test.asm"):
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
            self._test_ram_binary_content_helper(start=0, binary_content=binary_content, hex_content=hex_content)

        with mock.patch('builtins.input', return_value="../input/test3.asm"):
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
            self._test_ram_binary_content_helper(0, binary_content, hex_content)

    def assert_ram_content(self, start, content):
        """
        Verifies that actual output is aligned with the expected outputs
        :param start: starts reading RAM from given memory location as an int value
        :param content: binary/hexadecimal content to verify
        """
        for c in content:
            self.assertEqual(RAM[start] + RAM[start + 1], c, f'Verify line # {content.index(c) + 1}')
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


if __name__ == '__main__':
    unittest.main()
