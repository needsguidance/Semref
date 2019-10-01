from assembler import Assembler

asm = Assembler('input/test.asm')
asm.read_source()
for inst in asm.micro_instr:
    print(inst)
