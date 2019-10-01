from assembler import Assembler, RAM

asm = Assembler('input/test.asm')
asm.read_source()
asm.store_instructions_in_ram()
for mem in RAM[:50]:
    print(mem)
