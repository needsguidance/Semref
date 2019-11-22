import re


def convert_to_hex(num, bits):
    """
    Converts number to hexadecimal
    :param num: int
    :param bits: int
    :return: str
    """
    if not isinstance(num, int):
        raise ValueError("Invalid number type, num must be of type int.")
    return f'{num:0{int(bits / 4)}x}'.upper()


def convert_to_binary(num, bits):
    """
    Converts number to its binary representation
    :param num: int
    :param bits: str
    :return: str
    """
    if not isinstance(num, int):
        raise ValueError("Invalid number type, num must be of type int.")
    return f'{num:0{bits}b}'


def hex_to_binary(hex_num):
    """
    Converts hexadecimal number to binary
    :param hex_num: str
    :return: str
    """
    return f'{int(hex_num, 16):0{len(hex_num) * 4}b}'


def is_valid_port(port):
    """
    Verify if the port is available

    :param port: int
    :return: bool
    """

    return port not in RESERVED_PORTS


def update_reserved_ports(device, port_to_remove, port_to_add, reserve_block=False):
    """
    Update RESERVED_PORTS List.
    
    :param reserve_block: bool
    :param device: dict
    :param port_to_remove: int
    :param port_to_add: int
    """
    if not reserve_block:
        if port_to_remove in RESERVED_PORTS:
            RESERVED_PORTS.remove(port_to_remove)

        RESERVED_PORTS.append(port_to_add)
    else:
        for i in range(8):
            if port_to_add + i in RESERVED_PORTS:
                raise MemoryError('Illegal port')
        for i in range(8):
            if port_to_remove + i in RESERVED_PORTS:
                RESERVED_PORTS.remove(port_to_remove + i)

            RESERVED_PORTS.append(port_to_add + i)

    device['port'] = port_to_add


def update_indicators(instance, is_file_loaded):
    """
    This method manage Loaded/NotLoaded File indicators using a condition.
    :param instance: obj
    :param is_ram_loaded: bool
    """
    if is_file_loaded:
        instance.remove_widget(instance.not_loaded_file)
        instance.remove_widget(instance.loaded_file)
        instance.add_widget(instance.loaded_file)

    else:
        instance.remove_widget(instance.not_loaded_file)
        instance.remove_widget(instance.loaded_file)
        instance.add_widget(instance.not_loaded_file)


def clear_registers():
    value = '00'
    for key in REGISTER.keys():
        if key == 'cond':
            value = '0'
        elif key == 'pc' or key == 'sp':
            value = '000'
        elif key == 'ir':
            value = '0000'
        REGISTER[key] = value


def load_ram(data):
    """
    Loads data into RAM
    :param data: list
    """
    i = 0
    for item in data:
        item.strip()
        hex_instruction = ''.join(item.split())
        RAM[i] = hex_instruction[0:2]
        RAM[i + 1] = hex_instruction[2:]
        i += 2


def is_valid_file(filename):
    """
    Validates file is of type obj
    :param filename: str
    """
    return re.match(r'^.+\.?(obj|asm)$', filename) is not None, filename[-3:]


RAM = ['00' for i in range(4096)]

# OPCODE initialization list.
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
# Registers initialization.
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
    'ir': f'{0:04x}',
    'cond': f'{0:01x}'
}
# Format 1 of the different OPCODE.
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
# Format 2 of the different OPCODE.
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
# Format 3 of the different OPCODE.
FORMAT_3_OPCODE = [
    'jmpaddr',
    'jcondrin',
    'jcondaddr',
    'call'
]
# General Information of Traffic Light Object.
TRAFFIC_LIGHT = {
    'menu_title': 'Configure Traffic Light Port',
    'port': 0
}
# General Information of Seven Segment Display Object.
SEVEN_SEGMENT_DISPLAY = {
    'menu_title': 'Configure 7 Segment Display Port',
    'port': 1
}
# General Information of ASCII Table Object.
ASCII_TABLE = {
    'menu_title': 'Configure ASCII Table Port',
    'port': 3
}
# General Information of HEX Keyboard Object.
HEX_KEYBOARD = {
    'menu_title': 'Configure Hex Keyboard Port',
    'port': 2
}

# Reserved ports for I/O devices.
RESERVED_PORTS = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
]

EVENTS = {
    'IS_RAM_EMPTY': True
}
