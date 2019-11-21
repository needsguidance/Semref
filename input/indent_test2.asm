org 0
JMPADDR start
org 4
valor1 db 8
arreglo db 5, A, FF, 73
    const pi 31
org 0E
start:
    LOAD R1, valor1
    LOAD R2, arreglo
    LOADIM R3, pi
    GRT R1, R2
    JCONDADDR aca
    LOADIM R4,#0F
stay1:
    JMPADDR stay1
aca:
    LOADIM R4,#0A
stay2:
    JMPADDR stay2