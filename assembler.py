import re

from utils import OPCODE, convert_to_binary, RAM, is_valid_file

VARIABLES = {}
CONSTANTS = {}


def verify_ram_content():
    """
    Verifies ram is in binary format. If not will do the necessary changes to achieve this
    """
    i = 0
    for num in range(2048):
        if RAM[i] in ('jmprind', 'jcondrin'):
            opcode = OPCODE[RAM[i]]
            register_a = convert_to_binary(int(RAM[i + 1][1]), 3)
            binary = opcode + register_a + '00000000'
            RAM[i] = binary[0:8]
            RAM[i + 1] = binary[8:]
        elif RAM[i] in ('jmpaddr', 'jcondaddr', 'call'):
            opcode = OPCODE[RAM[i]]
            if RAM[i + 1] not in VARIABLES:
                address = f'{int(RAM[i + 1], 16):011b}'
            else:
                address = VARIABLES[RAM[i + 1]]
            binary = opcode + address if len(address) == 11 else address
            RAM[i] = binary[0:8]
            RAM[i + 1] = binary[8:]
        i += 2


def hexify_ram_content():
    """
    Converts binary content inside of RAM to hexadecimal
    """
    i = 0
    while i < len(RAM):
        try:
            RAM[i] = f'{int(RAM[i], 2):02X}'
        except (ValueError):
            print('assmbly')
        i += 1


def verify_indentation(line, index, file):
    """
    Verifies source code is indented properly
    :param line: str
    :param index: int
    :param file: obj
    """
    if "\t" in line:
        file.close()
        raise AssertionError(
            f'Indentation error on line {index + 1}: Tab detected.')
    if not is_indented(line) and line.startswith(" ") and not line.isspace():
        file.close()
        raise AssertionError(f'Indentation error: Line {index + 1}: Ensure that '
                             f'all indented lines have exactly 4 spaces.')
    if ":" in line and is_indented(line):
        file.close()
        raise AssertionError(
            f'Indentation error on line {index + 1}: Lines with \':\' cannot be indented.')
    if is_indented(line) and not contains_instruction(line):
        file.close()
        raise AssertionError(
            f"Indentation error on line {index + 1}: [org, db, const] instructions cannot be indented")
    if not is_indented(line) and contains_instruction(line):
        file.close()
        raise AssertionError(
            f'Indentation error: Line {index + 1}: Lines with instructions must be indented.')


def compare_indentation_between_lines(line1, line2, index, file):
    """
    Compares indentation between two lines
    :param line1: str
    :param line2: str
    :param index: int
    :param file: obj
    """
    if not is_indented(line2) and ":" in line1:
        file.close()
        raise AssertionError(
            f'Indentation Error: Line {index + 1}: lines under label must be indented.')


def is_indented(line):
    """
    Checks if line is indented
    :param line: str
    :return: bool
    """
    return line.startswith("    ") and not line[4].startswith(" ")


def contains_instruction(line):
    """
    Checks if the line contains an instruction defined in OPCODE
    :param line: str
    :return: bool
   """
    text = line.split()
    if text:
        return text[0].lower() in OPCODE
    return False


class Assembler:
    """Assembles assembly code"""

    def __init__(self, **kwargs):
        self.micro_instr = []  # Microprocessor instruction.
        self.p_counter = 0  # Program Counter.
        self.filename = kwargs.pop('filename', None)

    def read_source(self, filepath=None):
        """
        Reads source code and stores instructions a list
        :param filepath: obj
        """
        if filepath:
            self.filename = filepath
        is_valid, file_ext = is_valid_file(self.filename)

        if not is_valid and file_ext != 'asm':
            raise AssertionError(
                f'Unsupported file type [{self.filename}]. Only accepting files ending in .asm')
        source = open(self.filename, 'r')
        lines = source.readlines()

        # Removes comments from instructions
        for i in range(len(lines)):
            lines[i] = re.sub(r'//\s*(\w.+)*', '', lines[i])

        verify_indentation(lines[0], 0, source)
        self.micro_instr.append(lines[0].strip())
        for i in range(1, len(lines)):
            if lines[i] != '\n':
                verify_indentation(lines[i], i, source)
                compare_indentation_between_lines(
                    lines[i - 1], lines[i], i, source)
                self.micro_instr.append(lines[i].strip())
        lines.clear()
        source.close()

    def store_instructions_in_ram(self):
        """
        Stores instructions in ram
        """
        for instruction in self.micro_instr:
            if instruction:
                is_first_inst = self.micro_instr.index(instruction) == 0
                instruction = re.sub(',', ' ', instruction)
                source = instruction.split()
                contains_label = [s for s in source if ':' in s]
                if contains_label:
                    self.correct_p_counter()
                    label = source[0][:-1]
                    VARIABLES[label] = f'{self.p_counter:011b}'
                    if source[0].lower() in OPCODE:
                        raise SyntaxError('Invalid instruction')

                    if len(source) > 1:
                        self.convert_instruction_to_binary(source[1:])
                        self.p_counter += 2
                else:
                    if len(source) > 1 and 'db' not in source:
                        if source[0] != source[0].lower() and source[0] != source[0].upper():
                            raise SyntaxError(
                                "Syntax Error: Instructions written incorrectly.")
                    if is_first_inst:
                        self.p_counter = 0
                    if source[0].lower() == 'org':
                        # Indicates at what memory location it will begin storing instructions
                        if len(source) > 2:
                            # there is more than one value after the 'org' - invalid address.
                            raise SyntaxError(
                                "Too many arguments after 'org'.")

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
                        elif source[0].lower() == 'const':
                            const = f'{int(source[2], 16):08b}'
                            CONSTANTS[source[1]] = const

                        elif 'db' in source:
                            if source[0].lower() in OPCODE:
                                raise SyntaxError(
                                    f'{source[0].lower()} cannot be used as a variable')
                            VARIABLES[source[0]] = convert_to_binary(
                                self.p_counter, 8)
                            for i in range(2, len(source)):
                                RAM[self.p_counter] = convert_to_binary(
                                    int(source[i], 16), 8)
                                self.p_counter += 1
                        else:
                            raise SyntaxError(
                                f"'{instruction}' not a valid instruction")

    def convert_instruction_to_binary(self, inst):
        """
        Converts instruction to binary
        :param inst: str
        """
        instruction = inst[0].lower()
        if instruction.lower() in ('jmprind', 'jmpaddr', 'jcondrin', 'jcondaddr', 'call'):
            RAM[self.p_counter] = inst[0].lower()
            RAM[self.p_counter + 1] = inst[1]
        else:
            opcode = OPCODE[instruction]
            error = f"'{inst}' is an invalid instruction. Refer to manual for proper use."
            binary = f'{0:016b}'
            if instruction in ('load', 'loadim', 'addim', 'subim', 'loop'):
                if len(inst) != 3:
                    raise SyntaxError(error)
                register_a = convert_to_binary(
                    int(re.sub(r'[^\w\s]', '', inst[1])[1]), 3)
                if inst[2] in VARIABLES:
                    address_or_const = VARIABLES[inst[2]]
                elif inst[2] in CONSTANTS:
                    address_or_const = CONSTANTS[inst[2]]
                elif '#' in inst[2]:
                    address_or_const = convert_to_binary(
                        int(inst[2][1:], 16), 8)
                else:
                    address_or_const = convert_to_binary(
                        int(inst[2], 16), 8)
                binary = opcode + register_a + address_or_const
            elif instruction in ('pop', 'push'):
                if len(inst) != 2:
                    raise SyntaxError(error)
                register_a = convert_to_binary(
                    int(re.sub(r'[^\w\s]', '', inst[1])[1]), 3)
                binary = opcode + register_a + '00000000'
            elif instruction == 'store':
                if len(inst) != 3:
                    raise SyntaxError(error)
                register_a = convert_to_binary(
                    int(re.sub(r'[^\w\s]', '', inst[2])[1]), 3)
                variable = re.sub(r'[^\w\s]', '', inst[1])
                if variable not in VARIABLES:
                    address = convert_to_binary(int(variable, 16), 8)
                else:
                    address = VARIABLES[variable]
                binary = opcode + register_a + address
            elif instruction in ('loadrind', 'storerind', 'not', 'neg'):
                if len(inst) != 3:
                    raise SyntaxError(error)
                register_a = convert_to_binary(
                    int(re.sub(r'[^\w\s]', '', inst[1])[1]), 3)
                register_b = convert_to_binary(
                    int(re.sub(r'[^\w\s]', '', inst[2])[1]), 3)
                binary = opcode + register_a + register_b + '00000'
            elif instruction in ('add', 'sub', 'and', 'or', 'xor', 'shiftr', 'shiftl',
                                 'rotar', 'rotal'):
                if len(inst) != 4:
                    raise SyntaxError(error)
                register_a = re.sub(r'[^\w\s]', '', inst[1])
                register_b = re.sub(r'[^\w\s]', '', inst[2])
                register_c = re.sub(r'[^\w\s]', '', inst[3])
                if not re.match(r'^(R|r)[1-7]{1}$', register_a) or \
                        not re.match(r'^(R|r)[1-7]{1}$', register_b) or \
                        not re.match(r'^(R|r)[1-7]{1}$', register_c):
                    raise SyntaxError(f'Incorrect syntax for {inst}. Only accepts Register values')
                register_a = convert_to_binary(
                    int(register_a[1]), 3)
                register_b = convert_to_binary(
                    int(register_b[1]), 3)
                register_c = convert_to_binary(
                    int(register_c[1]), 3)
                binary = opcode + register_a + register_b + register_c + '00'
            elif instruction in ('grt', 'grteq', 'eq', 'neq'):
                if len(inst) != 3:
                    raise SyntaxError(error)
                register_a = convert_to_binary(
                    int(re.sub(r'[^\w\s]', '', inst[1])[1]), 3)
                register_b = convert_to_binary(
                    int(re.sub(r'[^\w\s]', '', inst[2])[1]), 3)
                binary = opcode + register_a + register_b + '00000'
            elif instruction in ('nop', 'return'):
                if len(inst) != 1:
                    raise SyntaxError(error)
                binary = opcode + '00000000000'
            RAM[self.p_counter] = binary[0:8]
            RAM[self.p_counter + 1] = binary[8:]

    def correct_p_counter(self):
        """
        Instructions must be stored in even memory addresses.
        Makes p_counter an even number if it is odd.
        """
        if self.p_counter % 2 != 0:
            self.p_counter += 1
