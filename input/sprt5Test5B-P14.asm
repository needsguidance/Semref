org 0
    JMPADDR start
org 100
semaforo db 0
org 110
sevenseg db 0
org 120
asciidisp1 db 0
asciidisp2 db 0
org 130
keyb db 0
org 10
start:
    LOADIM R5,#0A8
    STORE semaforo,R5 

    LOADIM R5,#0FF
    STORE semaforo,R5 

    LOADIM R5,#0F2
    STORE sevenseg,R5
    LOADIM R5,#0B7
    STORE sevenseg,R5

    LOAD R5,keyb
    LOAD R6,keyb
    ADDIM R5,#31
    ADDIM R6,#22
    STORE asciidisp1,R5
    STORE asciidisp2,R6