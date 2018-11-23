import my_consts as const

class CodeWriter:
    def __init__(self, fileName):
        self.jndex = 0
        self.setFileName(fileName)


    def setFileName(self, fileName):
        self.title = fileName.split('.')[0]
        self.title = self.title.split('/')[-1] if '/' in self.title else self.title
        self.file = open(fileName.split('.')[0] + '.asm', 'w')
        self.prepareMemory()


    def prepareMemory(self):
        self.file.write('(SP)\n@SP\n')
        self.file.write('(LCL)\n@LCL\n')
        self.file.write('(ARG)\n@ARG\n')
        self.file.write('(THIS)\n@THIS\n')
        self.file.write('(THAT)\n@THAT\n')


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
                if segment == const.STATIC:
                    self.file.write('@' + self.title + '.' + index + '\n')
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
                if segment == const.STATIC:
                    self.file.write('@' + self.title + '.' + index + '\n')
                self.file.write('D=D+M\n@R13\nM=D\n')
            self.file.write('@SP\nM=M-1\n@SP\nA=M\nD=M\n@R13\nA=M\nM=D\n')


    def close(self):
        self.file.close()
