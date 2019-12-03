//Probando org, db, load con variables, store, add, 
//brincos arriba y abajo, constante, 
//declaracion de constante
org 0
    JMPADDR principio
const tres 3
var1 db 5
var2 db 7, 9, 0B   //Revisar como quedan en memoria
principio:
    LOAD R1, var1  //Carga 5 a R1
    LOAD R2, var2  //Carga 7 a R2
    STORE var2, R1 //Guarda 5 en address 4
    ADD R3,R2,R1   //R3 <- 7 + 5 = 0C
    LOADIM R5, #0D //R5 <- #0D
    ADD R4,R5,R3 //R4 <- 0D + 0C = 19
cerca:             //Address 12 (hex)
    JMPADDR lejos
org 20
lejos:
    JMPADDR cerca  //At 00E <- A80CH ==1010100000001100B