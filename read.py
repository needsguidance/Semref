OPCODE = {
    'load': f'{0:05b}',
    'loadim': f'{1:05b}',
    'pop': f'{2:05b}',
    'store': f'{3:05b}',
    'push': f'{4:05b}',
    'loadrind': f'{5:05b}',
    'storerind': f'{6:05b}',
    'add': f'{7:05b}',
    'sub': f'{8:05b}',
    'addim': f'{9:05b}',
    'subim': f'{10:05b}',
    'and': f'{11:05b}',
    'or': f'{12:05b}',
    'xor': f'{13:05b}',
    'not': f'{14:05b}',
    'neg': f'{15:05b}',
    'shiftr': f'{16:05b}',
    'shiftl': f'{17:05b}',
    'rotar': f'{18:05b}',
    'rotal': f'{19:05b}',
    'jumprind': f'{20:05b}',
    'jumpaddr': f'{21:05b}',
    'jcondrin': f'{22:05b}',
    'jcondaddr': f'{23:05b}',
    'loop': f'{24:05b}',
    'grt': f'{25:05b}',
    'grteq': f'{26:05b}',
    'eq': f'{27:05b}',
    'neq': f'{28:05b}',
    'nop': f'{29:05b}',
    'call': f'{30:05b}',
    'return': f'{31:05b}'
}

REGISTER = {
    'r0': f'{0:03b}',
    'r1': f'{1:03b}',
    'r2': f'{2:03b}',
    'r3': f'{3:03b}',
    'r4': f'{4:03b}',
    'r5': f'{5:03b}',
    'r6': f'{6:03b}',
    'r7': f'{7:03b}'
}

file = open('input/input.txt', 'r')
lines = file.readlines()
for line in lines:
    print(line)
