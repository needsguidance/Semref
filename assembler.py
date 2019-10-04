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
ADDRESSES = { }
LABELS = { }
VARIABLES = { }
CONSTANTS = { }

# 4 KB RAM memory that stores assembly instructions to be simulated
RAM = ['00000000' for i in range(4096)]


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
            if len(source) < 2:
                # Placeholder for now. Should figure out a way to handle label addresses correctly!
                print("Hello World")
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
                    print(f'ORG: {org_address} MEM PC: {self.p_counter}')
                else:
                    if source[0].lower() in OPCODE:
                        # Assign instruction to proper memory location
                        # print('It is an assembly instruction')
                        for row in source:
                            if row.lower() in REGISTER:
                                #stores OPCODE + reg in memory
                                RAM[self.p_counter] = self.convert_instruction_to_binary(source[0].lower()) + self.convert_register_to_binary(row.lower()) 
                            elif len(source) == 2:
                                #stores OPCODE in p_counter and label address in p_counter+1
                                RAM[self.p_counter] = self.convert_instruction_to_binary(source[0].lower()) + '000'
                                RAM[self.p_counter+1] = f'{self.p_counter+1:08b}'
                                LABELS[source[1]] = f'{self.p_counter+1:08b}'
                            else:
                                RAM[self.p_counter]= self.convert_instruction_to_binary(source[0].lower()) + '000'                        

                    else:
                        if source[0].lower() == 'const':
                        #Checks for constants and stores them in Constant Dictionary. Then, stores in addresses the name of constant and p_counter as the address. then stores in memory p_counter as the address
                            CONSTANTS[source[1]] = f'{int(source[2], 16):08b}'
                            ADDRESSES[source[1]] = f'{self.p_counter:08b}'
                            RAM[self.p_counter] = f'{self.p_counter:08b}'

                        elif len(source) == 3:
                            #Stores variables same manner as constants
                            VARIABLES[source[0]] = f'{int(source[2]):08b}'
                            ADDRESSES[source[0]] = f'{self.p_counter:08b}'
                            RAM[self.p_counter] = f'{self.p_counter:08b}'




                    self.p_counter += 2  # Increase Program Counter
                    print('The current PC is: ' + str(self.p_counter))
        print(CONSTANTS)
        print(VARIABLES)
        print(LABELS)
        print(ADDRESSES)

    def display_ram_content(self):
        for row in RAM:
            print(row)


    def convert_all_to_binary(self):
        op = []
        reg = []
        inst = []
        i = 0
        print("\nChanging known instructions to binary: \n")
        for instruction in self.micro_instr:
            inst.append([])
            
            for row in instruction.split():
                row = re.sub(r'[^\w\s]','',row) #Remove punctuation from lines
                print(row)
           
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

            i+=1

        for row in inst:
            print(row)

    def convert_instruction_to_binary(self, inst):
        instBin = OPCODE.get(inst)
        return instBin
    
    def convert_register_to_binary(self, reg):
        regBin = REGISTER.get(reg)
        return regBin


             
                   

