from assembler import Assembler, RAM, verify_ram_content, hexify_ram_content

read_files = True
file = None
i = 0
while read_files:
    try:
        file = input('Input asm file path: ')
        asm = Assembler(file)
        asm.read_source()
        asm.store_instructions_in_ram()
        # asm.display_ram_content()
        asm.convert_all_to_binary()
        verify_ram_content()
        hexify_ram_content()
        f = open("output/out.obj", "w")
        for m in range(50):
            print(f'{RAM[i]} {RAM[i + 1]}')
            i += 2
            f.write(f'{RAM[i]} {RAM[i + 1]}'+'\n')
        f.close()

    except (AssertionError, FileNotFoundError, ValueError, MemoryError, KeyError) as e:
        print(e)
    keep_reading = str(input('\nInput another file? (Y/N): '))
    if keep_reading.lower() != 'y':
        read_files = not read_files
        i = 0
