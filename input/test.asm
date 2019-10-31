org 0
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
    STORE R2, mayor
    JMPADDR fin

R1esMayor:
    STORE R1, mayor
    LOADIM R3, #8

fin:
    JMPADDR fin
