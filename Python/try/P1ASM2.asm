; comentario número 1 =Programación=
        ORG %00001111 
Et1:    EQU $FFFF    
        LDAA #H     
        STAA @Et1
        INCA          
        STAA @Et1   
        INCA          
        STAA @Et1