import re
import my_consts as const


class CodeWriter:
    def __init__(self, fileName):
        self.jndex = 0
        self.functionName = None
        self.numOfReturns = 0
        if '.vm' in fileName:
            self.writeFile(fileName)
            self.prepareMemory()
        else:
            self.writeFile(fileName.rstrip('/') + '.asm')
            self.writeInit()


    def writeFile(self, fileName):
        self.setFileName(fileName)
        self.title = fileName.split('.')[0]
        self.title = self.title.split('/')[-1] if '/' in self.title else self.title
        if '.vm' in fileName:
            self.file = open(self.fileName + '.asm', 'w')
        else:
            self.file = open(self.fileName + '/' + fileName.split('.')[0] + '.asm', 'w')


    def setFileName(self, fileName):
        self.fileName = fileName.split('.')[0]


    def prepareMemory(self):
        self.file.write('(SP)\n@SP\n')
        self.file.write('(LCL)\n@LCL\n')
        self.file.write('(ARG)\n@ARG\n')
        self.file.write('(THIS)\n@THIS\n')
        self.file.write('(THAT)\n@THAT\n')


    def writeInit(self):
        self.file.write('// VM Bootstrap\n')
        self.file.write('(SP)\n@SP\n')
        self.file.write('(LCL)\n@LCL\n')
        self.file.write('(ARG)\n@ARG\n')
        self.file.write('(THIS)\n@THIS\n')
        self.file.write('(THAT)\n@THAT\n')
        self.file.write('@256\nD=A\n@SP\nM=D\n')
        self.file.write('@300\nD=A\n@LCL\nM=D\n')
        self.file.write('@400\nD=A\n@ARG\nM=D\n')
        # goto Sys.init
        #self.file.write('@' + self.title + '.Sys.init\n0;JMP\n')
        self.writeCall('Sys.init', '0', 'Sys.init')


    def writeLabel(self, label, vmCommand):
        self.file.write('// ' + vmCommand + '\n')
        if re.match(r'^\d', label) or not re.match(r'(\w|\:|\.)+', label):
            raise Exception('Label ' + label + ' is invalid!')
        else:
            if self.functionName is None:
                self.file.write('(' + label + ')\n')
            else:
                self.file.write('(' + self.functionName + '$' + label + ')\n')


    def writeGoto(self, label, vmCommand):
        self.file.write('// ' + vmCommand + '\n')
        if self.functionName is None:
            self.file.write('@' + label + '\n')
        else:
            self.file.write('@' + self.functionName + '$' + label + '\n')
        self.file.write('0;JMP\n')


    def writeIf(self, label, vmCommand):
        self.file.write('// ' + vmCommand + '\n')
        self.file.write('@SP\n')
        self.file.write('M=M-1\n')
        self.file.write('A=M\n')
        self.file.write('D=M\n')
        if self.functionName is None:
            self.file.write('@' + label + '\n')
        else:
            self.file.write('@' + self.functionName + '$' + label + '\n')
        self.file.write('D;JNE\n')


    def writeCall(self, functionName, numArguments, vmCommand):
        self.file.write('// ' + vmCommand + '\n')
        self.file.write('// push return-address\n')
        self.file.write('@' + functionName + '$' + str(self.numOfReturns) + 'return\nD=A\n')
        self.file.write('@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.file.write('// push LCL, ARG, THIS, THAT\n')
        self.file.write('@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.file.write('@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.file.write('@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.file.write('@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        self.file.write('// ARG = SP - n - 5\n')
        self.file.write('@5\nD=A\n@' + numArguments + '\nD=D+A\n')
        self.file.write('@SP\nD=M-D\n@ARG\nM=D\n')
        self.file.write('// LCL = SP\n')
        self.file.write('@SP\nD=M\n@LCL\nM=D\n')
        self.file.write('// goto f\n')
        self.file.write('@' + self.title + '.' + functionName + '\n0;JMP\n')
        self.file.write('// (return-address)\n')
        self.file.write('(' + functionName + '$' + str(self.numOfReturns) + 'return)\n')
        self.numOfReturns += 1


    def writeReturn(self, vmCommand):
        self.file.write('// ' + vmCommand + '\n')
        self.file.write('@LCL\nD=M\n@R14\nM=D\n')
        self.file.write('@5\nD=D-A\nA=D\nD=M\n@R15\nM=D\n')
        self.file.write('@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n')
        self.file.write('D=A+1\n@SP\nM=D\n')
        self.file.write('@R14\nA=M-1\nD=M\n@THAT\nM=D\n')
        self.file.write('@2\nD=A\n@R14\nA=M-D\nD=M\n@THIS\nM=D\n')
        self.file.write('@3\nD=A\n@R14\nA=M-D\nD=M\n@ARG\nM=D\n')
        self.file.write('@4\nD=A\n@R14\nA=M-D\nD=M\n@LCL\nM=D\n')
        self.file.write('@R15\nA=M\n0;JMP\n')


    def writeFunction(self, functionName, numLocals, vmCommand):
        self.file.write('// ' + vmCommand + '\n')
        if re.match(r'^\d', functionName) or not re.match(r'(\w|\:|\.)+', functionName):
            raise Exception('Label ' + functionName + ' is invalid!')
        else:
            self.functionName = functionName
            self.file.write('(' + self.title + '.' + functionName + ')\n')
            if numLocals != '0':
                self.file.write('@' + numLocals + '\nD=A\n(' + functionName + '$0initLocals)\n')
                self.file.write('D=D-1\n@LCL\nA=D+M\nM=0\n@' + functionName + '$0initLocals\n')
                self.file.write('D;JGT\n')
                self.file.write('@' + numLocals + '\nD=A\n@SP\nM=D+M\n')


    def writeArithmetic(self, command, vmCommand):
        self.file.write('// ' + vmCommand + '\n')
        self.file.write('@SP\nM=M-1\n')
        self.file.write('@SP\nA=M\n')
        if command == const.NEG:
            self.file.write('M=-M\n')
            self.file.write('@SP\nM=M+1\n')
            return
        if command == const.NOT:
            self.file.write('M=!M\n')
            self.file.write('@SP\nM=M+1\n')
            return
        self.file.write('D=M\n@SP\nM=M-1\nA=M\n')
        if command == const.ADD:
            self.file.write('M=D+M\n')
            self.file.write('@SP\nM=M+1\n')
            return
        if command == const.SUB:
            self.file.write('M=M-D\n')
            self.file.write('@SP\nM=M+1\n')
            return
        if command == const.AND:
            self.file.write('M=D&M\n')
            self.file.write('@SP\nM=M+1\n')
            return
        if command == const.OR:
            self.file.write('M=D|M\n')
            self.file.write('@SP\nM=M+1\n')
            return
        self.file.write('D=M-D\n')
        self.file.write('@TRUE' + str(self.jndex) + '\n')
        if command == const.EQ:
            self.file.write('D;JEQ\n')
        if command == const.GT:
            self.file.write('D;JGT\n')
        if command == const.LT:
            self.file.write('D;JLT\n')
        self.file.write('@SP\nA=M\n')
        self.file.write('M=0\n')
        self.file.write('@END' + str(self.jndex) + '\n')
        self.file.write('0;JMP\n')
        self.file.write('(TRUE' + str(self.jndex) + ')\n')
        self.file.write('@SP\nA=M\n')
        self.file.write('M=-1\n')
        self.file.write('(END' + str(self.jndex) + ')\n')
        self.jndex += 1
        self.file.write('@SP\nM=M+1\n')


    def writePushPop(self, command, segment, index, vmCommand):
        self.file.write('// ' + vmCommand + '\n')
        if command == const.PUSH:
            if segment == const.CONSTANT:
                self.file.write('@' + index + '\nD=A\n')
            elif segment == const.TEMP:
                self.file.write('@' + str(int(index) + 1) + '\nD=A\n')
                self.file.write('@THAT\nA=D+A\nD=M\n')
            elif segment == const.POINTER:
                if index == '0':
                    self.file.write('@THIS\n')
                if index == '1':
                    self.file.write('@THAT\n')
                self.file.write('D=M\n')
            elif segment == const.STATIC:
                self.file.write('@' + self.fileName + '.' + index + '\n')
                self.file.write('D=M\n')
            else:
                self.file.write('@' + index + '\nD=A\n')
                if segment == const.ARGUMENT:
                    self.file.write('@ARG\n')
                if segment == const.LOCAL:
                    self.file.write('@LCL\n')
                if segment == const.THIS:
                    self.file.write('@THIS\n')
                if segment == const.THAT:
                    self.file.write('@THAT\n')
                self.file.write('D=D+M\nA=D\nD=M\n')
            self.file.write('@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        if command == const.POP:
            if segment == const.TEMP:
                self.file.write('@' + str(int(index) + 1) + '\nD=A\n')
                self.file.write('@THAT\nD=D+A\n@R13\nM=D\n')
            elif segment == const.POINTER:
                if index == '0':
                    self.file.write('@THIS\n')
                if index == '1':
                    self.file.write('@THAT\n')
                self.file.write('D=A\n@R13\nM=D\n')
            elif segment == const.STATIC:
                self.file.write('@' + self.fileName + '.' + index + '\n')
                self.file.write('D=A\n@R13\nM=D\n')
            else:
                self.file.write('@' + index + '\nD=A\n')
                if segment == const.ARGUMENT:
                    self.file.write('@ARG\n')
                if segment == const.LOCAL:
                    self.file.write('@LCL\n')
                if segment == const.THIS:
                    self.file.write('@THIS\n')
                if segment == const.THAT:
                    self.file.write('@THAT\n')
                self.file.write('D=D+M\n@R13\nM=D\n')
            self.file.write('@SP\nM=M-1\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D\n')


    def close(self):
        self.file.close()
