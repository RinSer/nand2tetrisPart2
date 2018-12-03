// VM Bootstrap
(SP)
@SP
(LCL)
@LCL
(ARG)
@ARG
(THIS)
@THIS
(THAT)
@THAT
@256
D=A
@SP
M=D
@300
D=A
@LCL
M=D
@400
D=A
@ARG
M=D
// Sys.init
// push return-address
@Sys.init$0return
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL, ARG, THIS, THAT
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
// ARG = SP - n - 5
@5
D=A
@0
D=D+A
@SP
D=M-D
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@FibonacciElement.Sys.init
0;JMP
// (return-address)
(Sys.init$0return)
// function Main.fibonacci 0
(FibonacciElement.Main.fibonacci)
// push argument 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt                     // checks if n<2
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE0
D;JLT
@SP
A=M
M=0
@END0
0;JMP
(TRUE0)
@SP
A=M
M=-1
(END0)
@SP
M=M+1
// if-goto IF_TRUE
@SP
M=M-1
A=M
D=M
@Main.fibonacci$IF_TRUE
D;JNE
// goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP
// label IF_TRUE          // if n<2, return n
(Main.fibonacci$IF_TRUE)
// push argument 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@R14
M=D
@5
D=D-A
A=D
D=M
@R15
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
D=A+1
@SP
M=D
@R14
A=M-1
D=M
@THAT
M=D
@2
D=A
@R14
A=M-D
D=M
@THIS
M=D
@3
D=A
@R14
A=M-D
D=M
@ARG
M=D
@4
D=A
@R14
A=M-D
D=M
@LCL
M=D
@R15
A=M
0;JMP
// label IF_FALSE         // if n>=2, returns fib(n-2)+fib(n-1)
(Main.fibonacci$IF_FALSE)
// push argument 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
// call Main.fibonacci 1  // computes fib(n-2)
// push return-address
@Main.fibonacci$1return
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL, ARG, THIS, THAT
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
// ARG = SP - n - 5
@5
D=A
@1
D=D+A
@SP
D=M-D
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@FibonacciElement.Main.fibonacci
0;JMP
// (return-address)
(Main.fibonacci$1return)
// push argument 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
// call Main.fibonacci 1  // computes fib(n-1)
// push return-address
@Main.fibonacci$2return
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL, ARG, THIS, THAT
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
// ARG = SP - n - 5
@5
D=A
@1
D=D+A
@SP
D=M-D
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@FibonacciElement.Main.fibonacci
0;JMP
// (return-address)
(Main.fibonacci$2return)
// add                    // returns fib(n-1) + fib(n-2)
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
// return
@LCL
D=M
@R14
M=D
@5
D=D-A
A=D
D=M
@R15
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
D=A+1
@SP
M=D
@R14
A=M-1
D=M
@THAT
M=D
@2
D=A
@R14
A=M-D
D=M
@THIS
M=D
@3
D=A
@R14
A=M-D
D=M
@ARG
M=D
@4
D=A
@R14
A=M-D
D=M
@LCL
M=D
@R15
A=M
0;JMP
// function Sys.init 0
(FibonacciElement.Sys.init)
// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Main.fibonacci 1   // computes the 4'th fibonacci element
// push return-address
@Main.fibonacci$3return
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL, ARG, THIS, THAT
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
// ARG = SP - n - 5
@5
D=A
@1
D=D+A
@SP
D=M-D
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@FibonacciElement.Main.fibonacci
0;JMP
// (return-address)
(Main.fibonacci$3return)
// label WHILE
(Sys.init$WHILE)
// goto WHILE              // loops infinitely
@Sys.init$WHILE
0;JMP
