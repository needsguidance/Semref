//Probando alineamiento de instrucciones, 
//direccionamiento indirecto, R0 = 0
org 0
    JMPADDR start
var1 db 5
var2 db 0
var3 db 7
start:
    LOADIM R6,#2     //At 06 <- 0802 == 0000100000000010
    LOADRIND R5,R6   //R5 <- 05
    ADD R6,R6,R0     //R6 <- 2
    ADD R6,R6,R1     //R6 <- 3
    STORERIND R6,R6 //At 03 <- 03
    STORE var3, R5   //At 04 <- 05
    JMPADDR start