from assembler import Assembler

# file = input('Enter asm file: ')
asm = Assembler('input/test.asm')
asm.read_source()
asm.store_instructions_in_ram()
asm.convert_to_binary()
