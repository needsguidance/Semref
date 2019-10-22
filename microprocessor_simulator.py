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
        self.prev_index = -1
        self.counter = 0

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
        self.is_ram_loaded = True
        lines.clear()
        file.close()

    

    def disassembled_instruction(self):
        binary_instruction = hex_to_binary(f'{RAM[self.index]}{RAM[self.index + 1]}')
        return get_opcode_key(binary_instruction[0:5])

    def run_micro_instructions(self):
            REGISTER['ir'] = f'{RAM[self.index]}{RAM[self.index + 1]}'
            binary_instruction = hex_to_binary(f'{RAM[self.index]}{RAM[self.index + 1]}')
            self.execute_instruction(binary_instruction)

    def run_micro_instructions_step(self, step_index):
        if self.index == 0:
            f = open("output/debugger.txt", "w")
        else:
            f = open("output/debugger.txt", "a")
        REGISTER['ir'] = f'{RAM[self.index]}{RAM[self.index + 1]}'
        binary_instruction = hex_to_binary(f'{RAM[self.index]}{RAM[self.index + 1]}')
        self.execute_instruction(binary_instruction)
        if self.prev_index == self.index:
            self.is_running = False
        else:
            self.prev_index = self.index

        f.write("\n\n Instruction: " + (f'{self.index:02x}').upper() + ":" + f'{RAM[self.index]}' + ":" + "INSTRUCTION")
        f.write("\n\n Step " + str(step_index) + "\n\n")
        f.write("\n\n Register Content: \n\n")
        f.write(f'{REGISTER}')
        f.write("\n\n First 50 slots in memory: \n\n")
        i = 0
        for m in range(50):
            f.write(f'{RAM[i]} {RAM[i + 1]}' + '\n')
            i += 2
        f.close()

    def micro_clear(self):
        self.is_ram_loaded = False
        self.micro_instructions = []
        self.decoded_micro_instructions = []
        self.index = 0
        self.is_running = True
        self.cond = False
        self.prev_index = -1
        self.counter = 0
        for m in range(4096):
            RAM[m] = '00'

        for k, v in REGISTER.items():
            if k == 'pc' or k == 'sp':
                REGISTER[k] = f'{0:03x}'
            elif k == 'ir':
                REGISTER[k] = f'{0:04x}'
            else:
                REGISTER[k] = f'{0:02x}'

    def execute_instruction(self, instruction):
        if re.match('^[0]+$', instruction):
            self.micro_instructions.append('NOP')
        else:

            opcode = get_opcode_key(instruction[0:5])

            if opcode in FORMAT_1_OPCODE:
                ra = f'R{int(instruction[5:8], 2)}'
                rb = f'R{int(instruction[8:11], 2)}'
                rc = f'R{int(instruction[11:14], 2)}'
                if opcode == 'loadrind':
                    REGISTER[ra.lower()] = RAM[REGISTER[rb.lower()]]
                elif opcode == 'storerind':
                    REGISTER[rb.lower()] = RAM[REGISTER[ra.lower()]]
                elif opcode == 'grt':
                    self.cond = REGISTER[ra.lower()] > REGISTER[rb.lower()]
                elif opcode == 'add':
                    REGISTER[ra.lower()] = f'{int(REGISTER[rb.lower()], 16) + int(REGISTER[rc.lower()], 16):02x}'
                elif opcode == 'sub':
                    REGISTER[ra.lower()] = f'{REGISTER[rb.lower()] - REGISTER[rc.lower()]:02x}'
                elif opcode == 'and':
                    REGISTER[ra.lower()] = f'{REGISTER[rb.lower()] * REGISTER[rc.lower()]:02x}'
                elif opcode == 'or':
                    REGISTER[ra.lower()] = f'{REGISTER[rb.lower()] + REGISTER[rc.lower()]:02x}'
                elif opcode == 'xor':
                    _xor = REGISTER[rb.lower()] + REGISTER[rc.lower()] - 2 * REGISTER[rb.lower()] * REGISTER[rc.lower()]
                    REGISTER[ra.lower()] = f'{_xor:02x}'
                elif opcode == 'not':
                    REGISTER[ra.lower()] = f'{self.bit_not(hex_to_binary(REGISTER[rb.lower()])):02x}'
                elif opcode == 'neg':
                    REGISTER[ra.lower()] = f'{(-1) * REGISTER[rb.lower()]:02x}'
                elif opcode == 'shiftr':
                    REGISTER[ra.lower()] = f'{REGISTER[rb.lower()] >> REGISTER[rc.lower()]:02x}'
                elif opcode == 'shiftl':
                    REGISTER[ra.lower()] = f'{REGISTER[rb.lower()] << REGISTER[rc.lower()]:02x}'
                elif opcode == 'rotar':
                    _rotar = self.rotr(int(REGISTER[rb.lower()], 16), int(REGISTER[rc.lower()], 16))
                    REGISTER[ra.lower()] = f'{_rotar:02x}'
                elif opcode == 'rotal':
                    _rotl = self.rotl(int(REGISTER[rb.lower()], 16), int(REGISTER[rc.lower()], 16))
                    REGISTER[ra.lower()] = f'{_rotl:02x}'
                elif opcode == 'jmprind':
                    self.program_counter = int(REGISTER[ra.lower()], 16)
                elif opcode == 'grteq':
                    self.cond = int(REGISTER[ra.lower()], 16) >= int(REGISTER[rb.lower()], 16)
                elif opcode == 'eq':
                    self.cond = int(REGISTER[ra.lower()], 16) == int(REGISTER[rb.lower()], 16)
                elif opcode == 'neq':
                    self.cond = int(REGISTER[ra.lower()], 16) != int(REGISTER[rb.lower()], 16)
                elif opcode == 'nop':
                    # Do nothing
                    pass
                else:
                    self.micro_instructions.append(f'{opcode.upper()} {ra}, {rb}, {rc}')
                self.index += 2
                REGISTER['pc'] = f"{int(REGISTER['pc'], 16) + 2:03x}"
            elif opcode in FORMAT_2_OPCODE:
                ra = f'R{int(instruction[5:8], 2)}'
                address_or_const = int(instruction[8:], 2)
                if opcode == 'load' or 'loadim':
                    REGISTER[ra.lower()] = f'{int(RAM[address_or_const] + RAM[address_or_const + 1], 16):02x}'
                elif opcode == 'store':
                    RAM[self.index] = REGISTER[ra.lower()]
                elif opcode == 'addim':
                    _addim = int(REGISTER[ra], 16) + int(RAM[address_or_const] + RAM[address_or_const + 1], 16)
                    REGISTER[ra] = f'{_addim:02x}'
                elif opcode == 'subim':
                    _subim = int(REGISTER[ra], 16) - int(RAM[address_or_const] + RAM[address_or_const + 1], 16)
                    REGISTER[ra] = f'{_subim:02x}'
                elif opcode == 'pop':
                    REGISTER[ra.lower()] = RAM[REGISTER['sp']]
                    REGISTER['sp'] = f"{int(REGISTER['sp'], 16) + 1:03x}"
                elif opcode == 'push':
                    REGISTER['sp'] = f"{int(REGISTER['sp'], 16) - 1:03x}"
                    RAM[REGISTER['sp']] = REGISTER[ra.lower()]
                elif opcode == 'loop':
                    reg_ra = int(REGISTER[ra.lower()], 16) - 1
                    REGISTER[ra.lower()] = f'{reg_ra:02x}'
                    if reg_ra != 0:
                        REGISTER['sp'] = f'{address_or_const:03x}'
                self.index += 2
                REGISTER['pc'] = f"{int(REGISTER['pc'], 16) + 2:03x}"
            elif opcode in FORMAT_3_OPCODE:
                ra = f'R{int(instruction[5:8], 2)}'
                address = int(instruction[5:], 2)
                if opcode == 'jmpaddr':
                    self.index = address
                    REGISTER['pc'] = f'{address + 2:03x}'
                elif opcode == 'jcondrin':
                    REGISTER['pc'] = REGISTER[ra.lower()] if self.cond else f"{int(REGISTER['pc'], 16) + 2:03x}"
                elif opcode == 'jcondaddr':
                    REGISTER['pc'] = f'{address:03x}' if self.cond else f"{int(REGISTER['pc'], 16) + 2:03x}"
                elif opcode == 'call':
                    REGISTER['sp'] = f"{int(REGISTER['sp'], 16) - 2:03x}"
                    RAM[REGISTER['sp']] = REGISTER['pc']
                    REGISTER['pc'] = f'{address + 2:03x}'
            elif opcode == 'return':
                REGISTER['pc'] = RAM[REGISTER['sp']]
                REGISTER['sp'] = f"{int(REGISTER['sp'], 16) + 2:03x}"

    def bit_not(self, n, numbits=8):
        return (1 << numbits) - 1 - n

    def rotl(self, num, bits):
        bit = num & (1 << (bits - 1))
        num <<= 1
        if bit:
            num |= 1
        num &= (2 << bits - 1)

        return num

    def rotr(self, num, bits):
        num &= (2 << bits - 1)
        bit = num & 1
        num >>= 1
        if bit:
            num |= (1 << (bits - 1))

        return num
