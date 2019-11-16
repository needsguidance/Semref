org 0
JMPADDR start

start:
    LOADIM R1, #5
    LOADIM R3, #2
    LOADIM R5, #0A
    call multiply_by_four
    JMPRIND R5

multiply_by_four:
    SHIFTL R2, R1, R3
    RETURN
    
