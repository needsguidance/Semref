def convert_to_hex(num, bits):
    if not isinstance(num, int):
        raise ValueError("Invalid number type, num must be of type int.")
    return f'{num:0{int(bits / 4)}x}'


def hex_to_binary(hex_num):
    return f'{int(hex_num, 16):0{len(hex_num) * 4}b}'


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
    'jmprind': f'{20:05b}',
    'jmpaddr': f'{21:05b}',
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
    'r0': f'{0:02x}',
    'r1': f'{0:02x}',
    'r2': f'{0:02x}',
    'r3': f'{0:02x}',
    'r4': f'{0:02x}',
    'r5': f'{0:02x}',
    'r6': f'{0:02x}',
    'r7': f'{0:02x}',
    'pc': f'{0:03x}',
    'sp': f'{0:03x}',
    'ir': f'{0:04x}'
}

FORMAT_1_OPCODE = [
    'loadrind',
    'storerind',
    'add',
    'sub',
    'and',
    'or',
    'xor',
    'not',
    'neg',
    'shiftr',
    'shiftl',
    'rotar',
    'rotal',
    'jmprind',
    'grt',
    'grteq',
    'eq',
    'neq',
    'nop',

]

FORMAT_2_OPCODE = [
    'load',
    'loadim',
    'pop',
    'store',
    'push',
    'addim',
    'subim',
    'loop'
]

FORMAT_3_OPCODE = [
    'jmpaddr',
    'jcondrin',
    'jcondaddr',
    'call'
]

HEX_KEYBOARD = 4087
