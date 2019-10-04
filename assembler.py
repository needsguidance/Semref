import re, logging

logging.basicConfig(level=logging.DEBUG)  # for debug purpose.

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
    'jumprind': f'{20:05b}',
    'jumpaddr': f'{21:05b}',
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

# 4 KB RAM memory that stores assembly instructions to be simulated
RAM = ['00000000' for i in range(4096)]


class Assembler:

    def __init__(self, filename):
        self.filename = filename
        self.micro_instr = []  # Microprocessor instruction.
        self.p_counter = 0  # Program Counter.

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

    def is_hex_number(self, number):
        return not isinstance(number, int)

    def store_instructions_in_ram(self):
        for instruction in self.micro_instr:
            source = instruction.split()
            if len(source) < 2:
                # Placeholder for now. Should figure out a way to handle label addresses correctly!
                print("Hello World")
            else:
                if source[0].lower() == 'org':
                    # Indicates at what memory location it will begin storing instructions
                    org_address = source[1]
                    if self.is_hex_number(org_address):
                        self.p_counter = int(org_address, 16)
                    else:
                        org_address = f'0x{org_address}'
                        self.p_counter = int(org_address, 16)

                    print(f'ORG: {org_address} MEM PC: {self.p_counter}')
                else:
                    if source[0].lower() in OPCODE:
                        # Assign instruction to proper memory location
                        print('It is an assembly instruction')
                    else:
                        print(source)

                    self.p_counter += 2  # Increase Program Counter
                    print('The current PC is: ' + str(self.p_counter))
                    # logging.debug('The current PC is: ' + str(self.p_counter))



