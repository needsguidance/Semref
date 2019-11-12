from assembler import RAM as ASSEMBLER_RAM
from microprocessor_simulator import RAM as SIM_RAM, MicroSim
from assembler import Assembler, verify_ram_content, hexify_ram_content

def clear_ram():
    for i in range(4096):
        ASSEMBLER_RAM[i] = '00000000'
        SIM_RAM[i] = '00000000'

def assert_ram_content(tester, content, RAM):
        """
        Verifies that actual output is aligned with the expected outputs
        :param start: starts reading RAM from given memory location as an int value
        :param content: binary/hexadecimal content to verify
        """
        for c in content:
            tester.assertEqual(RAM[c[1]] + RAM[c[1] + 1],
                             c[0], f'Verify line # {content.index(c) + 1} "{c}"')

def verify_ram_content_helper(tester, instance):
        """
        Helper to test different input files and verify expected outputs vs actual outputs
        """
        filename = input()
        clear_ram()
        if isinstance(instance, Assembler):
            instance.micro_instr.clear()
            instance.read_source(filename)
            instance.store_instructions_in_ram()

            verify_ram_content()
            assert_ram_content(tester, tester.binary_content, ASSEMBLER_RAM)

            hexify_ram_content()
            assert_ram_content(tester, tester.hex_content, ASSEMBLER_RAM)
        else:
            instance.read_obj_file(filename)
            while instance.is_running:
                instance.run_micro_instructions()
                if instance.prev_index == instance.index:
                    instance.is_running = False
                else:
                    instance.prev_index = instance.index
            assert_ram_content(tester, tester.ram_content, SIM_RAM)
            instance.index = 0
            instance.prev_index = -1