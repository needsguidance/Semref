org 0E
    NOP
    LOADIM R1, #5
    LOADIM R5, #AC
    LOADIM R6, #79
    ROTAR R3, R5, R1
    ROTAL R4, R6, R1
    GRTEQ R3, R4
    JMPADDR greater

    greater:
    XOR R1, R3, R4
    NOT R3, R3
    NEG R4, R4

fin:
    JMPADDR fin
