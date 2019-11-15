org 0
start:
	JMPADDR begin
x	db 0
y	db A
z	db F
begin:
	LOADIM R5, #C
	LOAD R6, z
	NEQ R6,R5
	LOAD R7, x
	ADDIM R7, #1
	STORE x, R7
	JCONDRIN R0
fin:
	JMPADDR fin