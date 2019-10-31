org 1001
JMPADDR start

valor1 db 5
valor2 db 7
mayor  db 0
const ten 0A

start:
    LOAD R1, valor1
    LOAD R2, valor2
    GRT  R1, R2
    JMPADDR R1esMayor
    STORE mayor, R2
    JMPADDR fin

R1esMayor:
    STORE mayor, R1
    LOADIM R3, 8

fin:
    JMPADDR fin