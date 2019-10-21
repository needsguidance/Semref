import re

from constants import OPCODE, FORMAT_1_OPCODE, FORMAT_2_OPCODE, FORMAT_3_OPCODE, REGISTER

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
        self.cond = False

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
                ra = f'R{int(instruction[5:8], 2)}'
                rb = f'R{int(instruction[8:11], 2)}'
                rc = f'R{int(instruction[11:14], 2)}'
                if opcode == 'loadrind' or opcode == 'storerind':
                    self.micro_instructions.append(f'{opcode.upper()} {ra}, {rb}')
                elif opcode == 'grt':
                    self.cond = REGISTER[ra] > REGISTER[rb]
                elif opcode == 'add':
                    REGISTER[ra] = REGISTER[rb] + REGISTER[rc]
                elif opcode == 'sub':
                    REGISTER[ra] = REGISTER[rb] - REGISTER[rc]
                elif opcode == 'and':
                    REGISTER[ra] = REGISTER[rb] * REGISTER[rc]
                elif opcode == 'or':
                    REGISTER[ra] = REGISTER[rb] + REGISTER[rc]
                elif opcode == 'xor':
                    REGISTER[ra] = REGISTER[rb] + REGISTER[rc] - 2 * REGISTER[rb] * REGISTER[rc]
                elif opcode == 'not':
                    REGISTER[ra] = self.bit_not(REGISTER[rb])
                elif opcode == 'neg':
                    REGISTER[ra] = (-1)*REGISTER[rb]
                elif opcode == 'shiftr':
                    REGISTER[ra] = REGISTER[rb] >> REGISTER[rc]
                elif opcode == 'shiftl':
                    REGISTER[ra] = REGISTER[rb] << REGISTER[rc]
                elif opcode == 'rotar':
                    REGISTER[ra] = self.rotr(REGISTER[rb], REGISTER[rc])
                elif opcode == 'rotal':
                    REGISTER[ra] = self.rotl(REGISTER[rb], REGISTER[rc])

                else:
                    self.micro_instructions.append(f'{opcode.upper()} {ra}, {rb}, {rc}')
                self.index += 2
            elif opcode in FORMAT_2_OPCODE:
                ra = f'R{int(instruction[5:8], 2)}'
                address_or_const = int(instruction[8:], 2)
                if opcode == 'load':
                    REGISTER[ra.lower()] = int(RAM[address_or_const] + RAM[address_or_const + 1], 16)
                elif opcode == 'store':
                    RAM[self.index] = REGISTER[ra.lower()]
                elif opcode == 'addim':
                    REGISTER[ra] = REGISTER[ra] + int(RAM[address_or_const] + RAM[address_or_const + 1], 16)
                elif opcode == 'subim':
                    REGISTER[ra] = REGISTER[ra] - int(RAM[address_or_const] + RAM[address_or_const + 1], 16)
                self.index += 2
            elif opcode in FORMAT_3_OPCODE:
                address = instruction[5:]
                self.index = int(address, 2)
                # self.micro_instructions.append(f'{opcode.upper()} {address}')
    
    def bit_not(n, numbits=8):
        return (1 << numbits) - 1 - n
    
    def rotl(num, bits):
        bit = num & (1 << (bits-1))
        num <<= 1
        if(bit):
            num |= 1
        num &= (2<<bits-1)

        return num

    def rotr(num, bits):
        num &= (2<<bits-1)
        bit = num & 1
        num >>= 1
        if(bit):
            num |= (1 << (bits-1))

        return num
