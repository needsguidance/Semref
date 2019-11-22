import re
import time

from utils import (FORMAT_1_OPCODE, FORMAT_2_OPCODE, FORMAT_3_OPCODE, OPCODE,
                   REGISTER, clear_registers, convert_to_hex, hex_to_binary, RAM, load_ram, is_valid_file, clear_ram)


def get_opcode_key(val):
    """
    Gets the opcode for the given value
    """
    for key, value in OPCODE.items():
        if val == value:
            return key
    return None


class MicroSim:
    """Microprocessor simulator"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_ram_loaded = False
        self.decoded_micro_instructions = []
        self.program_counter = 0
        self.is_running = False
        self.prev_program_counter = -1
        self.counter = 0
        self.filename = ''
        self.error = ''

    def read_obj_file(self, filename):
        """
        Reads obj file and stores content in RAM
        :param filename: str
        """
        is_valid, file_ext = is_valid_file(filename)
        if not is_valid and file_ext != 'obj':
            raise AssertionError(
                f"Unsupported file '{filename}'. "
                f"Microprocesor simulator files must be of type 'obj'")
        self.filename = filename

        file = open(filename, 'r')
        lines = file.readlines()
        load_ram(lines)

        self.is_ram_loaded = True
        lines.clear()
        file.close()

    def disassembled_instruction(self):
        """Disassembles executed assembly instruction"""
        instruction = hex_to_binary(f'{RAM[self.program_counter]}{RAM[self.program_counter + 1]}')
        opcode = get_opcode_key(instruction[0:5])
        if opcode in FORMAT_1_OPCODE:
            register_a = f'R{int(instruction[5:8], 2)}'
            register_b = f'R{int(instruction[8:11], 2)}'
            register_c = f'R{int(instruction[11:14], 2)}'
            if opcode == 'nop':
                dis_instruction = f'{opcode}'
            elif opcode == 'jmprind':
                dis_instruction = f'{opcode} {register_a}'
            elif opcode in ('loadrind', 'storerind', 'not', 'neg', 'grt', 'grteq', 'eq', 'neq'):
                dis_instruction = f'{opcode} {register_a}, {register_b}'
            else:
                dis_instruction = f'{opcode} {register_a}, {register_b}, {register_c}'
        elif opcode in FORMAT_2_OPCODE:
            register_a = f'R{int(instruction[5:8], 2)}'
            address_or_const = f'{int(instruction[8:], 2):02x}'
            if opcode in ('pop', 'push'):
                dis_instruction = f'{opcode} {register_a}'
            elif opcode in ('loadim', 'addim', 'subim'):
                dis_instruction = f'{opcode} {register_a}, #{address_or_const}'
            else:
                dis_instruction = f'{opcode} {register_a}, {address_or_const}'
        elif opcode in FORMAT_3_OPCODE:
            register_a = f'R{int(instruction[5:8], 2)}'
            address = f'{int(instruction[5:], 2):02x}'
            if opcode == 'jcondrin':
                dis_instruction = f'{opcode} {register_a}'
            else:
                dis_instruction = f'{opcode} {address}'
        else:
            dis_instruction = f'{opcode}'
        return dis_instruction.upper()

    def run_micro_instructions(self, timeout=0):
        """
        Runs assembly instructions
        :param timeout: int
        """
        if timeout != 0 and time.time() > timeout:
            self.is_running = False
            raise TimeoutError('Infinite loop detected.')
        REGISTER['ir'] = f'{RAM[self.program_counter]}{RAM[self.program_counter + 1]}'
        binary_instruction = hex_to_binary(
            f'{RAM[self.program_counter]}{RAM[self.program_counter + 1]}')
        self.execute_instruction(binary_instruction)
        if self.prev_program_counter == self.program_counter:
            self.is_running = False
        else:
            self.prev_program_counter = self.program_counter

    def micro_clear(self):
        """
        Resets microprocessor simulator to initial conditions
        """
        self.is_ram_loaded = False
        self.decoded_micro_instructions = []
        self.program_counter = 0
        self.is_running = False
        self.prev_program_counter = -1
        self.counter = 0
        clear_ram()
        clear_registers()

    def execute_instruction(self, instruction):
        """
        Executes assembly instruction
        :param instruction: str
        """
        if re.match('^[0]+$', instruction):
            self.prev_program_counter = self.program_counter
            self.program_counter += 2
            REGISTER['pc'] = convert_to_hex(self.program_counter, 3)
        else:
            opcode = get_opcode_key(instruction[0:5])

            if opcode in FORMAT_1_OPCODE:
                ra = f'r{int(instruction[5:8], 2)}'
                rb = f'r{int(instruction[8:11], 2)}'
                rc = f'r{int(instruction[11:14], 2)}'
                if opcode == 'loadrind':
                    REGISTER[ra] = RAM[int(REGISTER[rb], 16)]
                elif opcode == 'storerind':
                    RAM[int(REGISTER[ra], 16)] = REGISTER[rb]
                elif opcode == 'grt':
                    _grt = int(REGISTER[ra] > REGISTER[rb])
                    REGISTER['cond'] = convert_to_hex(_grt, 4)
                elif opcode == 'add':
                    _add = int(REGISTER[rb], 16) + int(REGISTER[rc], 16)
                    REGISTER[ra] = convert_to_hex(_add, 8)
                elif opcode == 'sub':
                    _sub = int(REGISTER[rb], 16) - int(REGISTER[rc], 16)
                    REGISTER[ra] = convert_to_hex(_sub, 8)
                elif opcode == 'and':
                    _and = int(REGISTER[rb]) & int(REGISTER[rc])
                    REGISTER[ra] = convert_to_hex(_and, 8)
                elif opcode == 'or':
                    _or = int(REGISTER[rb]) | int(REGISTER[rc])
                    REGISTER[ra] = convert_to_hex(_or, 8)
                elif opcode == 'xor':
                    _xor = int(REGISTER[rb]) ^ int(REGISTER[rc])
                    REGISTER[ra] = convert_to_hex(_xor, 8)
                elif opcode == 'not':
                    _not = self.bit_not(int(REGISTER[rb], 16)) + 1
                    REGISTER[ra] = convert_to_hex(_not, 8)
                elif opcode == 'neg':
                    _neg = self.bit_not(int(REGISTER[rb], 16))
                    REGISTER[ra] = convert_to_hex(_neg, 8)
                elif opcode == 'shiftr':
                    _shiftr = int(REGISTER[rb], 16) >> int(REGISTER[rc], 16)
                    REGISTER[ra] = convert_to_hex(_shiftr, 8)
                elif opcode == 'shiftl':
                    _shiftl = int(REGISTER[rb], 16) << int(REGISTER[rc], 16)
                    REGISTER[ra] = convert_to_hex(_shiftl, 8)
                elif opcode == 'rotar':
                    _rotar = self.rotr(int(REGISTER[rb], 16), int(
                        REGISTER[rc], 16))
                    REGISTER[ra] = convert_to_hex(_rotar, 8)
                elif opcode == 'rotal':
                    _rotl = self.rotl(int(REGISTER[rb], 16), int(
                        REGISTER[rc], 16))
                    REGISTER[ra] = convert_to_hex(_rotl, 8)
                elif opcode == 'jmprind':
                    self.program_counter = int(REGISTER[ra], 16) - 2
                    REGISTER['pc'] = f'{self.program_counter:03x}'
                elif opcode == 'grteq':
                    REGISTER['cond'] = str(int(int(REGISTER[ra], 16) >= int(
                        REGISTER[rb], 16)))
                elif opcode == 'eq':
                    REGISTER['cond'] = str(int(int(REGISTER[ra], 16) == int(
                        REGISTER[rb], 16)))
                elif opcode == 'neq':
                    REGISTER['cond'] = str(int(int(REGISTER[ra], 16) != int(
                        REGISTER[rb], 16)))
                self.program_counter += 2
                REGISTER['pc'] = convert_to_hex(
                    int(REGISTER['pc'], 16) + 2, 12)
                if REGISTER['r0'] != '00':
                    raise SystemError('R0 cannot be modified')
            elif opcode in FORMAT_2_OPCODE:
                ra = f'r{int(instruction[5:8], 2)}'
                address_or_const = int(instruction[8:], 2)
                if opcode == 'load':
                    REGISTER[ra] = convert_to_hex(
                        int(RAM[address_or_const], 16), 8)
                elif opcode == 'loadim':
                    REGISTER[ra] = convert_to_hex(address_or_const, 8)
                elif opcode == 'store':
                    RAM[int(RAM[address_or_const], 16)] = REGISTER[ra]
                elif opcode == 'addim':
                    _addim = int(REGISTER[ra], 16) + address_or_const
                    REGISTER[ra] = convert_to_hex(_addim, 8)
                elif opcode == 'subim':
                    _subim = int(REGISTER[ra], 16) - address_or_const
                    REGISTER[ra] = convert_to_hex(_subim, 8)
                elif opcode == 'pop':
                    sp = int(REGISTER['sp'], 16)
                    REGISTER[ra] = RAM[sp]
                    sp += 1
                    if sp >= len(RAM):
                        sp -= len(RAM)
                    REGISTER['sp'] = convert_to_hex(sp, 12)
                elif opcode == 'push':
                    sp = int(REGISTER['sp'], 16) - 1
                    if sp < 0:
                        sp += len(RAM)
                    REGISTER['sp'] = convert_to_hex(sp, 12)
                    RAM[sp] = REGISTER[ra]
                elif opcode == 'loop':
                    reg_ra = int(REGISTER[ra], 16) - 1
                    REGISTER[ra] = convert_to_hex(reg_ra, 8)
                    if reg_ra != 0:
                        REGISTER['pc'] = convert_to_hex(
                            address_or_const - 2, 12)
                        self.program_counter = address_or_const - 2
                        self.prev_program_counter = self.program_counter - 2
                self.program_counter += 2
                REGISTER['pc'] = convert_to_hex(
                    int(REGISTER['pc'], 16) + 2, 12)
            elif opcode in FORMAT_3_OPCODE:
                ra = f'r{int(instruction[5:8], 2)}'
                address = int(instruction[5:], 2)
                if opcode == 'jmpaddr':
                    self.program_counter = address
                    REGISTER['pc'] = convert_to_hex(address, 12)
                elif opcode == 'jcondrin':
                    REGISTER['pc'] = REGISTER[ra] if int(REGISTER['cond']) else convert_to_hex(
                        int(REGISTER['pc'], 16) + 2,
                        12)
                    self.program_counter = int(REGISTER['pc'], 16)
                elif opcode == 'jcondaddr':
                    REGISTER['pc'] = convert_to_hex(address, 12) if int(REGISTER['cond']) \
                        else convert_to_hex(int(REGISTER['pc'], 16) + 2, 12)
                    self.program_counter = int(REGISTER['pc'], 16)
                elif opcode == 'call':
                    sp = int(REGISTER['sp'], 16) - 2
                    if sp < 0:
                        sp += len(RAM)
                    RAM[sp] = f'0{REGISTER["pc"][0]}'
                    RAM[sp + 1] = REGISTER["pc"][1:]
                    REGISTER['sp'] = convert_to_hex(sp, 12)
                    REGISTER['pc'] = convert_to_hex(address, 12)
                    self.program_counter = address
            elif opcode == 'return':
                sp = int(REGISTER['sp'], 16)
                pc = RAM[sp][1] + RAM[sp + 1]
                REGISTER['pc'] = convert_to_hex(int(pc) + 2, 12)
                sp += 2
                if sp >= len(RAM):
                    sp -= len(RAM)
                REGISTER['sp'] = convert_to_hex(sp, 12)
                self.program_counter = int(REGISTER['pc'], 16)

    def bit_not(self, n, numbits=8):
        """
        1's complementing a binary number up to the given amount of bits
        :param n: int
        :param numbits: int
        """
        return (1 << numbits) - 1 - n

    def rotl(self, num, bits):
        """
        Rotates bits to the left
        :param num: int
        :param bits: int
        """
        bit = num & (1 << (bits - 1))
        num <<= 1
        if bit:
            num |= 1
        num &= (2 << bits - 1)

        return num

    def rotr(self, num, bits):
        """
        Rotates bits to the right
        :param num: int
        :param bits: int
        """
        num &= (2 << bits - 1)
        bit = num & 1
        num >>= 1
        if bit:
            num |= (1 << (bits - 1))
        return num
