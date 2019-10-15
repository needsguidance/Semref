class MicroSim:

    def read_obj_file(self, filename):
        file = open(filename, 'r')
        lines = file.readlines()
        for line in lines:
            print(line)
        lines.clear()
        file.close()
