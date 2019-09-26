OPCODE = {
    'load': hex(0),
    'loadim': hex(1),
    'pop': hex(2),
    'store': hex(3),
    'push': hex(4),
    'loadrind': hex(5),
    'storerind': hex(6),
    'add': hex(7),
    'sub': hex(8),
    'addim': hex(9),
    'subim': hex(10),
    'and': hex(11),
    'or': hex(12),
    'xor': hex(13),
    'not': hex(14),
    'neg': hex(15),
    'shiftr': hex(16),
    'shiftl': hex(17),
    'rotar': hex(18),
    'rotal': hex(19),
    'jumprind': hex(20),
    'jumpaddr': hex(21),
    'jcondrin': hex(22),
    'jcondaddr': hex(23),
    'loop': hex(24),
    'grt': hex(25),
    'grteq': hex(26),
    'eq': hex(27),
    'neq': hex(28),
    'nop': hex(29),
    'call': hex(30),
    'return': hex(31)
}

REGISTER = {
    'r0': hex(0),
    'r1': hex(1),
    'r2': hex(2),
    'r3': hex(3),
    'r4': hex(4),
    'r5': hex(5),
    'r6': hex(6),
    'r7': hex(7)
}

file = open('input/input.txt', 'r')
lines = file.readlines()
for line in lines:
    print(line)
