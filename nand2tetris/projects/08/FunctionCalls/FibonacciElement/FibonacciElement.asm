@256
D=A
@SP
M=D
@sys.init.1.cretn
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@sys.init
0;JMP
(sys.init.1.cretn)
(main.fibonacci)
@0
D=A
@R13
M=D
(main.fibonacci_loop0)
@R13
M=M-1
D=M
@main.fibonacci_loop1
D;JLT
D=0
@SP
A=M
M=D
@SP
M=M+1
@main.fibonacci_loop0
0;JMP
(main.fibonacci_loop1)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@R14
D=0
M=!D
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
D=D-M
@Main.1
D;JLT
@R14
M=0
(Main.1)
@R14
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@Main.if_true
D;JNE
@Main.if_false
0;JMP
(Main.if_true)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R13
M=D
@ARG
D=M
@SP
M=D
@R13
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R14
M=D
@R14
M=M-1
A=M
D=M
@THAT
M=D
@R14
M=M-1
A=M
D=M
@THIS
M=D
@R14
M=M-1
A=M
D=M
@ARG
M=D
@R14
M=M-1
A=M
D=M
@LCL
M=D
@R14
M=M-1
A=M
A=M
0;JMP
(Main.if_false)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
D=D-M
@SP
A=M
M=D
@SP
M=M+1
@main.fibonacci.2.cretn
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@main.fibonacci
0;JMP
(main.fibonacci.2.cretn)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
D=D-M
@SP
A=M
M=D
@SP
M=M+1
@main.fibonacci.3.cretn
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@main.fibonacci
0;JMP
(main.fibonacci.3.cretn)
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
D=D+M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@R13
M=D
@ARG
D=M
@SP
M=D
@R13
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R14
M=D
@R14
M=M-1
A=M
D=M
@THAT
M=D
@R14
M=M-1
A=M
D=M
@THIS
M=D
@R14
M=M-1
A=M
D=M
@ARG
M=D
@R14
M=M-1
A=M
D=M
@LCL
M=D
@R14
M=M-1
A=M
A=M
0;JMP
(sys.init)
@0
D=A
@R13
M=D
(sys.init_loop0)
@R13
M=M-1
D=M
@sys.init_loop1
D;JLT
D=0
@SP
A=M
M=D
@SP
M=M+1
@sys.init_loop0
0;JMP
(sys.init_loop1)
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
@main.fibonacci.1.cretn
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@main.fibonacci
0;JMP
(main.fibonacci.1.cretn)
(Sys.while)
@Sys.while
0;JMP
