from assembler import RAM

def assert_ram_content(tester, content):
        """
        Verifies that actual output is aligned with the expected outputs
        :param start: starts reading RAM from given memory location as an int value
        :param content: binary/hexadecimal content to verify
        """
        for c in content:
            tester.assertEqual(RAM[c[1]] + RAM[c[1] + 1],
                             c[0], f'Verify line # {content.index(c) + 1} "{c}"')