org 0
    JMPADDR start
mayor db 0
suma  db 0
start:
    LOADIM R0,#03
    LOADIM R2,#05
    LOADIM R3,#00
again:
    ADD R3,R3,R2
    SUBIM R2,#01
    NEQ R2,R0
    JCONDADDR again
    STORE suma,R3
stay:
    JMPADDR stay