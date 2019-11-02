import unittest

import mock

from assembler import Assembler, verify_ram_content, RAM, hexify_ram_content, clear_ram


class InputTestCase(unittest.TestCase):

    def test_invalid_input(self):
        with mock.patch('builtins.input', return_value='input.txt'):
            file = input()
            with self.assertRaises(AssertionError):
                Assembler(file)

        with mock.patch('builtins.input', return_value='test.asm'):
            file = input()
            asm = Assembler(file)
            with self.assertRaises(FileNotFoundError):
                asm.read_source()

    def test_valid_input(self):
        with mock.patch('builtins.input', return_value="input/test.asm"):
            file = input()
            asm = Assembler(file)
            self.assertEqual(file, asm.filename, 'Filenames do not match')


if __name__ == '__main__':
    unittest.main()
