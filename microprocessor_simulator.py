import re

from constants import OPCODE, FORMAT_1_OPCODE, FORMAT_2_OPCODE, FORMAT_3_OPCODE

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
        self.index = 0
        self.is_running = True

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
        while self.is_running:
            binary_instruction = hex_to_binary(f'{RAM[self.index]}{RAM[self.index + 1]}')
            self.decode_instruction(binary_instruction)
            # print(instruction)

    def decode_instruction(self, instruction):
        if re.match('^[0]+$', instruction):
            self.micro_instructions.append('NOP')
        else:
            opcode = get_opcode_key(instruction[0:5])
            if opcode in FORMAT_1_OPCODE:
                ra = int(instruction[5:8], 2)
                rb = int(instruction[8:11], 2)
                rc = int(instruction[11:14], 2)
                if opcode == 'loadrind' or opcode == 'storerind' or opcode == 'grt':
                    self.micro_instructions.append(f'{opcode.upper()} R{ra}, R{rb}')
                else:
                    self.micro_instructions.append(f'{opcode.upper()} R{ra}, R{rb}, R{rc}')
            elif opcode in FORMAT_2_OPCODE:
                ra = int(instruction[5:8], 2)
                address_or_const = instruction[8:]
                self.micro_instructions.append(f'{opcode.upper()} R{ra}, {address_or_const}')
            elif opcode in FORMAT_3_OPCODE:
                address = instruction[5:]

                self.micro_instructions.append(f'{opcode.upper()} {address}')
