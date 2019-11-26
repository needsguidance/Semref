org 0
    jmp start

valor1 db 5
valor2 db 7
mayor  db 0
const ten 0A

AnotherOne:
    ADD R1, R3
    JMP fin

start:
    LOAD R1, valor1
    LOAD R2, valor2
    GRT  R1, R2
    JMP AnotherOne

R1esMayor:
    STORE mayor, R1
    LOADIM R3, #8

fin:
    JMP fin