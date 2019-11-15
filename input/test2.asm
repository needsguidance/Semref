org 2 3
JMPADDR start

valor1 db 5
valor2 db 7

fin:
    JMPADDR fin

start:
    LOAD R1, valor1
	LOAD R2, valor2
	ADD  R1, R2
    JMPADDR fin

