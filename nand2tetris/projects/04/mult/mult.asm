// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.



M[16]=0
M[2]=0

(LOOP)

D=M[0]

D=D-M[16]

@LOOPEND
D;JLE

D=M[1]
D=M[2]+D
M[2]=D

D=M[16];
M[16]=D+1

@LOOP
0;JMP

(LOOPEND)

(END)
@END
0;JMP