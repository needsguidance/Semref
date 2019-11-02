import re

from constants import OPCODE, REGISTER, convert_to_binary

ADDRESSES = {}
LABELS = {}
VARIABLES = {}
CONSTANTS = {}

# 4 KB RAM memory that stores assembly instructions to be simulated
RAM = ['00000000' for i in range(4096)]


def clear_ram():
    for i in range(len(RAM)):
        RAM[i] = '00000000'


def verify_ram_content():
    i = 0
    for num in range(2048):
        if RAM[i] == 'jmprind' or RAM[i] == 'jcondrin':
            opcode = OPCODE[RAM[i]]
            ra = REGISTER[RAM[i + 1]]
            binary = opcode + ra + '00000000'
            RAM[i] = binary[0:8]
            RAM[i + 1] = binary[8:]
        elif RAM[i] == 'jmpaddr' or RAM[i] == 'jcondaddr':
            opcode = OPCODE[RAM[i]]
            address = f'{int(RAM[i + 1], 16):011b}' if RAM[i + 1] not in VARIABLES else VARIABLES[RAM[i + 1]]
            binary = opcode + address if len(address) == 11 else address
            RAM[i] = binary[0:8]
            RAM[i + 1] = binary[8:]
        i += 2


def hexify_ram_content():
    for i in range(4096):
        RAM[i] = f'{int(RAM[i], 2):02X}'


class Assembler:

    def __init__(self, filename):
        self.filename = filename
        self.micro_instr = []  # Microprocessor instruction.
        self.p_counter = 0  # Program Counter.
        self.filename = filename
        if not self.is_valid_source():
            raise AssertionError(f'Unsupported file type [{self.filename}]. Only accepting files ending in .asm')

    def read_source(self):
        if self.is_valid_source():
            source = open(self.filename, 'r')
            lines = source.readlines()
            for line in lines:
                if line != '\n':
                    self.micro_instr.append(line.strip())
            lines.clear()
            source.close()

    def is_valid_source(self):
        return re.match(r'^.+\.asm$', self.filename)

    def store_instructions_in_ram(self):
        for instruction in self.micro_instr:

            source = instruction.split()
            contains_label = [s for s in source if ':' in s]
            if contains_label:
                self.correct_p_counter()
                label = source[0][:-1]
                VARIABLES[label] = f'{self.p_counter:011b}'
                if len(source) > 1:
                    self.convert_instruction_to_binary(source[1:])
                    self.p_counter += 2
            else:
                if source[0].lower() == 'org':
                    # Indicates at what memory location it will begin storing instructions
                    if len(source) > 2:
                        # there is more than one value after the 'org' - invalid address.
                        raise SyntaxError("Too many arguments after 'org'.")

                    org_address = int(source[1], 16)

                    if org_address > 4096 or org_address < 0:
                        # the number given is not within the possible values (0 to 4096).
                        raise MemoryError('Exceeded Memory Size')

                    self.p_counter = org_address
                else:
                    if source[0].lower() in OPCODE:
                        self.correct_p_counter()
                        # Assign instruction to proper memory location
                        self.convert_instruction_to_binary(source)
                        self.p_counter += 2  # Increase Program Counter
                    else:
                        if source[0].lower() == 'const':
                            const = f'{int(source[2], 16):08b}'
                            CONSTANTS[source[1]] = const

                        elif len(source) == 3:
                            VARIABLES[source[0]] = f'{self.p_counter:08b}'
                            RAM[self.p_counter] = f'{int(source[2]):08b}'
                            self.p_counter += 1
                        else:
                            raise SyntaxError(f"'{instruction}' not a valid instruction")

    def convert_instruction_to_binary(self, inst, is_second_pass=False):
        if not is_second_pass:
            instruction = inst[0].lower()
            if instruction.lower() == 'jmprind' or instruction.lower() == 'jmpaddr' or \
                    instruction.lower() == 'jcondrin' or instruction.lower() == 'jcondaddr' or \
                    instruction.lower() == 'call':
                RAM[self.p_counter] = inst[0].lower()
                RAM[self.p_counter + 1] = inst[1]
            else:
                opcode = OPCODE[instruction]
                error = f"'{inst}' is an invalid instruction. Refer to manual for proper use."
                binary = f'{0:016b}'
                if instruction == 'load' or instruction == 'loadim' or instruction == 'addim' or \
                        instruction == 'subim' or instruction == 'loop':
                    if len(inst) != 3:
                        raise SyntaxError(error)
                    ra = convert_to_binary(int(re.sub(r'[^\w\s]', '', inst[1])[1]), 3)
                    if inst[2] in VARIABLES:
                        address_or_const = VARIABLES[inst[2]]
                    elif inst[2] in CONSTANTS:
                        address_or_const = CONSTANTS[inst[2]]
                    elif '#' in inst[2]:
                        address_or_const = convert_to_binary(int(inst[2][1:]), 8)
                    else:
                        address_or_const = convert_to_binary(int(inst[2]), 8)
                    binary = opcode + ra + address_or_const
                elif instruction == 'pop' or instruction == 'push':
                    if len(inst) != 2:
                        raise SyntaxError(error)
                    ra = convert_to_binary(int(re.sub(r'[^\w\s]', '', inst[1])[1]), 3)
                    binary = opcode + ra + '00000000'
                elif instruction == 'store':
                    if len(inst) != 3:
                        raise SyntaxError(error)
                    ra = convert_to_binary(int(re.sub(r'[^\w\s]', '', inst[2])[1]), 3)
                    variable = re.sub(r'[^\w\s]', '', inst[1])
                    address = convert_to_binary(int(variable), 8) if variable not in VARIABLES else VARIABLES[variable]
                    binary = opcode + ra + address
                elif instruction == 'loadrind' or instruction == 'storerind' or instruction == 'not' or \
                        instruction == 'neg':
                    if len(inst) != 3:
                        raise SyntaxError(error)
                    ra = convert_to_binary(int(re.sub(r'[^\w\s]', '', inst[1])[1]), 3)
                    rb = convert_to_binary(int(re.sub(r'[^\w\s]', '', inst[2])[1]), 3)
                    binary = opcode + ra + rb + '00000'
                elif instruction == 'add' or instruction == 'sub' or instruction == 'and' or \
                        instruction == 'or' or instruction == 'xor' or instruction == 'shiftr' or \
                        instruction == 'shiftl' or instruction == 'rotar' or instruction == 'rotal':
                    if len(inst) != 4:
                        raise SyntaxError(error)
                    ra = convert_to_binary(int(re.sub(r'[^\w\s]', '', inst[1])[1]), 3)
                    rb = convert_to_binary(int(re.sub(r'[^\w\s]', '', inst[2])[1]), 3)
                    rc = convert_to_binary(int(re.sub(r'[^\w\s]', '', inst[3])[1]), 3)
                    binary = opcode + ra + rb + rc + '00'
                elif instruction == 'grt' or instruction == 'grteq' or instruction == 'eq' or instruction == 'neq':
                    if len(inst) != 3:
                        raise SyntaxError(error)
                    ra = convert_to_binary(int(re.sub(r'[^\w\s]', '', inst[1])[1]), 3)
                    rb = convert_to_binary(int(re.sub(r'[^\w\s]', '', inst[2])[1]), 3)
                    binary = opcode + ra + rb + '00000'
                elif instruction == 'nop' or instruction == 'return':
                    if len(inst) != 1:
                        raise SyntaxError(error)
                    binary = opcode + '00000000000'
                RAM[self.p_counter] = binary[0:8]
                RAM[self.p_counter + 1] = binary[8:]

        # instBin = OPCODE.get(inst)
        # return instBin

    def correct_p_counter(self):
        """
        Instructions must be stored in even memory addresses. Makes p_counter an even number if it is odd.
        """
        if self.p_counter % 2 != 0:
            self.p_counter += 1
