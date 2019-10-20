import re

from constants import OPCODE

RAM = ['00' for i in range(4096)]


def hex_to_binary(hex_instruction):
    return f'{int(hex_instruction, 16):016b}'


def get_opcode_key(val):
    for key, value in OPCODE.items():
        if val == value:
            return key
    return None


class MicroSim:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_ram_loaded = False
        self.micro_instructions = []
        self.decoded_micro_instructions = []

    def read_obj_file(self, filename):
        file = open(filename, 'r')
        lines = file.readlines()
        i = 0
        for line in lines:
            line.strip()
            hex_instruction = ''.join(line.split())
            RAM[i] = hex_instruction[0:2]
            RAM[i + 1] = hex_instruction[2:]
            i += 2
            # self.micro_instructions.append(hex_to_binary(hex_instruction))
        self.is_ram_loaded = True
        lines.clear()
        file.close()

    def run_micro_instructions(self):
        index = 0
        for i in range(int(len(RAM) / 2)):
            binary_instruction = hex_to_binary(f'{RAM[index]}{RAM[index + 1]}')
            self.decode_instruction(binary_instruction)
            index += 2
            # print(instruction)

    def decode_instruction(self, instruction):
        if re.match('^[0]+$', instruction):
            print('nop')
        else:
            opcode = get_opcode_key(instruction[0:5])
            print(opcode)
