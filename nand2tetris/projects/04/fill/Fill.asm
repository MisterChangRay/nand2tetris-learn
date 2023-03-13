// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


@24576
D=A
M[0]=D

@16384
D=A
M[1]=D
M[8]=D

@32222
D=A
M[2]=D

(LOOP)

D=M[1]
D=M[0]-D
@RESET
D;JLT


@0
D=A
M[3]=D


D=M[24576]
@SET0
D;JLT 

@SET1
D;JGT


(SET0)
D=M[3]
M[4]=D
@START
0;JMP

(SET1)
D=M[2]
M[4]=D


(START)


D=M[4]
A=M[1]
M=D

D=M[1]
M[1]=D+1


D=M[0]
D=D-M[1]


@LOOP
0;JMP


(RESET)
D=M[8]
M[1]=D
@LOOP
0;JMP