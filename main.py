from assembler import Assembler

file = input('Enter asm file: ')
asm = Assembler(file)
asm.read_source()
asm.store_instructions_in_ram()
