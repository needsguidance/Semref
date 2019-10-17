class MicroSim:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hex_instructions = []

    def read_obj_file(self, filename):
        file = open(filename, 'r')
        lines = file.readlines()
        for line in lines:
            self.hex_instructions.append(line)
        lines.clear()
        file.close()
