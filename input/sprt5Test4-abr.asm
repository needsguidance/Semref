org 0
mayor db 0
menor db 0
LOADIM R0,#03
LOADIM R2,#04
LOADIM R3,#0A
LOADIM R4,#0F
GRT R2,R3
JCONDADDR R2mayor
ADD R5,R0,R3
JMPADDR R3mayor
R2mayor:
    ADD R5,R0,R2
R3mayor: 
    GRTEQ R4,R5
    JCONDADDR R4mayor
    JMPADDR fin
R4mayor:
    ADD R5,R0,R4
fin:
    STORE mayor,R5
    JMPRIND R2