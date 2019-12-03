//sprt5Test1.asm
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
    STORE var2, R1 //Guarda 5 en address 3
    LOADIM R5,#05  //R5 <- 57
    LOADIM R6,#05  //R6 <- 57
    LOADIM R4,#02  
    SHIFTR R5,R5,R4
    ROTAR R5,R5,R4
cerca:             //Address 16 (hex)
    JMPADDR lejos  //
org 50
lejos:
    JMPADDR cerca  //At 012 <- A80CH ==1010100000010000B