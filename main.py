from assembler import Assembler

asm = Assembler('input/test.asm')
asm.read_source()
print(asm.micro_instr)
