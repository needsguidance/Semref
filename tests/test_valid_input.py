import unittest

import mock

from assembler import Assembler
from microprocessor_simulator import MicroSim


class InputTestCase(unittest.TestCase):

    def test_invalid_input(self):
        instance = MicroSim()
        with mock.patch('builtins.input', return_value='input.txt'):
            file = input()
            with self.assertRaises(AssertionError):
                instance.read_obj_file(file)

        with mock.patch('builtins.input', return_value='test.asm'):
            file = input()
            asm = Assembler(filename=file)
            with self.assertRaises(FileNotFoundError):
                asm.read_source()

        with mock.patch('builtins.input', return_value='input.txt'):
            file = input()
            with self.assertRaises(AssertionError):
                instance.read_obj_file(file)

    def test_valid_input(self):
        with mock.patch('builtins.input', return_value="input/test.asm"):
            file = input()
            asm = Assembler(filename=file)
            self.assertEqual(file, asm.filename, 'Filenames do not match')


if __name__ == '__main__':
    unittest.main()
