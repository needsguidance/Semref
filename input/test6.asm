org 0
JMPADDR start:
    a    db A
    b    db B
    suma db 0
    resta db 0
    and db 0
start:
    LOADIM R1, #5
    LOADIM R2, #F
    ADD R3, R1, R2
    STORE suma, R3
    SUB R3, R1, R2
    STORE resta, R3
    AND R3, R1, R2
    STORE and, R3
fin:
    JMPADDR fin