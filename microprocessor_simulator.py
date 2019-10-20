class MicroSim:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.micro_instructions = []

    def read_obj_file(self, filename):
        file = open(filename, 'r')
        lines = file.readlines()
        for line in lines:
            line.strip()
            hex_instruction = ''.join(line.split())
            # hex_instructions = line.split()
            self.micro_instructions.append(self.hex_to_binary(hex_instruction))
        lines.clear()
        file.close()
    
    def hex_to_binary(self, hex_instruction):
        return f'{int(hex_instruction, 16):016b}'
