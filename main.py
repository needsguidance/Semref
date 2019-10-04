from assembler import Assembler

read_files = True
file = None
while read_files:
    try:
        file = input('Input asm file path: ')
        asm = Assembler(file)
        asm.read_source()
        asm.store_instructions_in_ram()
        # asm.display_ram_content()
        asm.convert_all_to_binary()
    except (AssertionError, FileNotFoundError, ValueError, MemoryError) as e:
        print(e)
    keep_reading = str(input('\nInput another file? (Y/N): '))
    if keep_reading.lower() != 'y':
        read_files = not read_files
