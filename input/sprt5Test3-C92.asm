org 0
start:
    LOADIM R2,#03
    LOADIM R7,#100
    CALL fun
    PUSH R5
    PUSH R6
    POP R5
    POP R6
    LOOP R2, start
fun:
    LOADIM R3,#05
    LOADIM R4,#0F
    AND R5,R3,R4
    OR R6,R3,R4
    RETURN