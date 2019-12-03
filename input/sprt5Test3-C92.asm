//sprt5Test3.asm
//Operaciones con el stack y loop
org 0
start:
    LOADIM R7,#100  //SP <- 100
    CALL fun
    PUSH R5         //Revisar stack
    PUSH R6         //Revisar stack
    POP R5          //R5 <- 0F
    POP R6          //R6 <- 05
    LOOP R6, start
fun:
    LOADIM R3,#05   //R3 <- 05
    LOADIM R4,#0F   //R4 <- 0F
    AND R5,R3,R4    //R5 <- 05
    OR R6,R3,R4     //R6 <- 0F
    RETURN