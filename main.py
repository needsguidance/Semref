from assembler import Assembler, RAM, verify_ram_content, hexify_ram_content
from microprocessor_simulator import MicroSim
from GUI.window import TestApp


def assembler():
    read_files = False
    file = None
    i = 0
    while read_files:
        try:
            file = input('Input asm file path: ')
            asm = Assembler(file)
            asm.read_source()
            asm.store_instructions_in_ram()
            verify_ram_content()
            hexify_ram_content()
            f = open("output/out.obj", "w")
            for m in range(50):
                print(f'{RAM[i]} {RAM[i + 1]}')
                f.write(f'{RAM[i]} {RAM[i + 1]}' + '\n')
                i += 2
            f.close()
        except (AssertionError, FileNotFoundError, ValueError, MemoryError, KeyError, SyntaxError) as e:
            print(e)
        keep_reading = str(input('\nInput another file? (Y/N): '))
        if keep_reading.lower() != 'y':
            read_files = not read_files
            i = 0


def micro_sim():
    read_files = False
    i = 0
    while read_files:
        file = input('Input obj file path: ')
        sim = MicroSim()
        sim.read_obj_file(file)


# assembler()  # Test assembler
micro_sim()
TestApp().run()  # Comment this code to test assembler/microprocessor simulator
