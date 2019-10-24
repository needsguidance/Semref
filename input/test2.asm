    org 0
    JMPADDR start
a   db A
b   db B
suma db 0
resta db 0
start:
    LOADIM R1, 5
    LOADIM R2, F
    ADD R3, R1, R2
    STORE R3, suma
    SUB R3, R1, R2
    STORE R3, resta
    AND R3, R1, R2
fin:
    JMPADDR fin