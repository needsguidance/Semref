org 0
LOADIM R1, #5
LOADIM R2, #2
LOADIM R3, #1
PUSH R1
SHIFTL R4, R2, R3
LOOP R1, 0A
POP R1
LOADRIND R5, R1
STORERIND R1, R6


