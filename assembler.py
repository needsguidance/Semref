import re

OPCODE = {
    'load': f'{0:05b}',
    'loadim': f'{1:05b}',
    'pop': f'{2:05b}',
    'store': f'{3:05b}',
    'push': f'{4:05b}',
    'loadrind': f'{5:05b}',
    'storerind': f'{6:05b}',
    'add': f'{7:05b}',
    'sub': f'{8:05b}',
    'addim': f'{9:05b}',
    'subim': f'{10:05b}',
    'and': f'{11:05b}',
    'or': f'{12:05b}',
    'xor': f'{13:05b}',
    'not': f'{14:05b}',
    'neg': f'{15:05b}',
    'shiftr': f'{16:05b}',
    'shiftl': f'{17:05b}',
    'rotar': f'{18:05b}',
    'rotal': f'{19:05b}',
    'jmprind': f'{20:05b}',
    'jmpaddr': f'{21:05b}',
    'jcondrin': f'{22:05b}',
    'jcondaddr': f'{23:05b}',
    'loop': f'{24:05b}',
    'grt': f'{25:05b}',
    'grteq': f'{26:05b}',
    'eq': f'{27:05b}',
    'neq': f'{28:05b}',
    'nop': f'{29:05b}',
    'call': f'{30:05b}',
    'return': f'{31:05b}'
}

REGISTER = {
    'r0': f'{0:03b}',
    'r1': f'{1:03b}',
    'r2': f'{2:03b}',
    'r3': f'{3:03b}',
    'r4': f'{4:03b}',
    'r5': f'{5:03b}',
    'r6': f'{6:03b}',
    'r7': f'{7:03b}'
}
ADDRESSES = {}
LABELS = {}
VARIABLES = {}
CONSTANTS = {}

# 4 KB RAM memory that stores assembly instructions to be simulated
RAM = ['00000000' for i in range(4096)]


def clear_ram():
    for i in range(len(RAM)):
        RAM[i] = '00000000'

def display_ram_content():
    for row in RAM:
        print(row)


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

                    org_address = source[1]

                    if int(org_address, 16) > 4096:
                        # the number given is not within the possible values (0 to 4096).
                        raise MemoryError('Exceeded Memory Size')

                    self.p_counter = int(org_address, 16)
                else:
                    if source[0].lower() in OPCODE:
                        # Assign instruction to proper memory location
                        self.convert_instruction_to_binary(source)

                    else:
                        if source[0].lower() == 'const':
                            const = f'{int(source[2], 16):016b}'
                            msb = const[0:8]
                            lsb = const[8:]
                            VARIABLES[source[1]] = self.p_counter
                            RAM[self.p_counter] = msb
                            RAM[self.p_counter + 1] = lsb

                        elif len(source) == 3:
                            VARIABLES[source[0]] = f'{self.p_counter:08b}'
                            RAM[self.p_counter] = f'{int(source[2]):08b}'
                        else:
                            raise SyntaxError(f"'{instruction}' not a valid instruction")


                    self.p_counter += 2  # Increase Program Counter

    # def convert_all_to_binary(self):
    #     inst = []
    #
    #     for instruction in self.micro_instr:
    #         source = instruction.split()
    #         i = 0
    #         for row in source:
    #             if row.lower() in OPCODE:
    #                 inst[i].append(OPCODE.get(row))
    #             elif row.lower() in REGISTER:
    #                 inst[i].append(REGISTER.get(row))
    #             elif row.lower() in LABELS:
    #                 inst[i].append(LABELS.get(row))
    #             elif row.lower() in ADDRESSES:
    #                 inst[i].append(ADDRESSES.get(row))
    #
    #             i += 1

    def convert_all_to_binary(self):
        op = []
        reg = []
        inst = []
        i = 0
        for instruction in self.micro_instr:
            inst.append([])

            for row in instruction.split():
                row = re.sub(r'[^\w\s]', '', row)  # Remove punctuation from lines

                if row.lower() in OPCODE:
                    inst[i].append(OPCODE.get(row.lower()))
                elif row.lower() in REGISTER:
                    inst[i].append(REGISTER.get(row.lower()))
                elif row in LABELS:
                    inst[i].append(LABELS.get(row))
                elif row in ADDRESSES:
                    inst[i].append(ADDRESSES.get(row))
                else:
                    inst[i].append(row)

            i += 1

    def convert_instruction_to_binary(self, inst, is_second_pass=False):
        if not is_second_pass:
            if inst[0].lower() == 'jmprind' or inst[0].lower() == 'jmpaddr' or inst[0].lower() == 'jcondrin' or \
                    inst[0].lower() == 'jcondaddr':
                RAM[self.p_counter] = inst[0].lower()
                RAM[self.p_counter + 1] = inst[1]
            else:
                instruction = inst[0].lower()
                opcode = OPCODE[instruction]
                binary = f'{0:016b}'
                if instruction == 'loadrind' or instruction == 'storerind' or instruction == 'add' or \
                        instruction == 'sub' or instruction == 'and' or instruction == 'or' or instruction == 'xor' or \
                        instruction == 'not' or instruction == 'neg' or instruction == 'shiftr' or \
                        instruction == 'shiftl' or instruction == 'rotar' or instruction == 'rotal' or \
                        instruction == 'grt' or instruction == 'grteq' or instruction == 'eq' or instruction == 'neq':
                    ra = REGISTER[re.sub(r'[^\w\s]', '', inst[1]).lower()]
                    rb = REGISTER[re.sub(r'[^\w\s]', '', inst[2]).lower()]
                    rc = f'{0:03b}' if len(inst) == 3 else REGISTER[re.sub(r'[^\w\s]', '', inst[3]).lower()]
                    binary = opcode + ra + rb + rc + '00'
                elif instruction == 'load' or instruction == 'loadim' or instruction == 'pop' or \
                        instruction == 'store' or instruction == 'push' or instruction == 'addim' or \
                        instruction == 'subim' or instruction == 'loop':
                    ra = REGISTER[re.sub(r'[^\w\s]', '', inst[1]).lower()]
                    address = f'{int(inst[2], 16):08b}' if inst[2] not in VARIABLES else VARIABLES[inst[2]]
                    binary = opcode + ra + address
                elif instruction == 'call':
                    address = f'{int(inst[2], 16):011b}' if inst[2] not in VARIABLES else VARIABLES[inst[2]]
                    binary = opcode + address
                RAM[self.p_counter] = binary[0:8]
                RAM[self.p_counter + 1] = binary[8:]

        # instBin = OPCODE.get(inst)
        # return instBin

    def convert_register_to_binary(self, reg):
        regBin = REGISTER.get(reg)
        return regBin
