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
(class1.set)
@0
D=A
@R13
M=D
(class1.set_loop0)
@R13
M=M-1
D=M
@class1.set_loop1
D;JLT
D=0
@SP
A=M
M=D
@SP
M=M+1
@class1.set_loop0
0;JMP
(class1.set_loop1)
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
@Class1.0
M=D
@1
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
@Class1.1
M=D
@0
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
@LCL
D=M
@5
A=D-A
D=M
@R14
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
@1
A=D-A
D=M
@THAT
M=D
@LCL
D=M
@2
A=D-A
D=M
@THIS
M=D
@LCL
D=M
@3
A=D-A
D=M
@ARG
M=D
@LCL
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
(class1.get)
@0
D=A
@R13
M=D
(class1.get_loop0)
@R13
M=M-1
D=M
@class1.get_loop1
D;JLT
D=0
@SP
A=M
M=D
@SP
M=M+1
@class1.get_loop0
0;JMP
(class1.get_loop1)
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@Class1.1
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
@SP
M=M-1
A=M
D=M
@R13
M=D
@LCL
D=M
@5
A=D-A
D=M
@R14
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
@1
A=D-A
D=M
@THAT
M=D
@LCL
D=M
@2
A=D-A
D=M
@THIS
M=D
@LCL
D=M
@3
A=D-A
D=M
@ARG
M=D
@LCL
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
(class2.set)
@0
D=A
@R13
M=D
(class2.set_loop0)
@R13
M=M-1
D=M
@class2.set_loop1
D;JLT
D=0
@SP
A=M
M=D
@SP
M=M+1
@class2.set_loop0
0;JMP
(class2.set_loop1)
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
@Class2.0
M=D
@1
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
@Class2.1
M=D
@0
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
@LCL
D=M
@5
A=D-A
D=M
@R14
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
@1
A=D-A
D=M
@THAT
M=D
@LCL
D=M
@2
A=D-A
D=M
@THIS
M=D
@LCL
D=M
@3
A=D-A
D=M
@ARG
M=D
@LCL
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
(class2.get)
@0
D=A
@R13
M=D
(class2.get_loop0)
@R13
M=M-1
D=M
@class2.get_loop1
D;JLT
D=0
@SP
A=M
M=D
@SP
M=M+1
@class2.get_loop0
0;JMP
(class2.get_loop1)
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@Class2.1
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
@SP
M=M-1
A=M
D=M
@R13
M=D
@LCL
D=M
@5
A=D-A
D=M
@R14
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
@1
A=D-A
D=M
@THAT
M=D
@LCL
D=M
@2
A=D-A
D=M
@THIS
M=D
@LCL
D=M
@3
A=D-A
D=M
@ARG
M=D
@LCL
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
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
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
@class1.set.1.cretn
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
@7
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@class1.set
0;JMP
(class1.set.1.cretn)
@SP
M=M-1
A=M
D=M
@R5
M=D
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
@class2.set.2.cretn
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
@7
D=A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@class2.set
0;JMP
(class2.set.2.cretn)
@SP
M=M-1
A=M
D=M
@R5
M=D
@class1.get.3.cretn
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
@class1.get
0;JMP
(class1.get.3.cretn)
@class2.get.4.cretn
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
@class2.get
0;JMP
(class2.get.4.cretn)
(Sys.while)
@Sys.while
0;JMP