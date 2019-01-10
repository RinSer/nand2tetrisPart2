class VMWriter:
    def __init__(self, fileName):
        self.out = open(fileName + '.vm', 'w')

    def writePush(self, segment, index):
        self.out.write('push ' + segment + ' ' + str(index) + '\n')

    def writePop(self, segment, index):
        self.out.write('pop ' + segment + ' ' + str(index) + '\n')

    def writeArithmetic(self, command, unary = False):
        if unary:
            command = {
                '-': 'neg',
                '~': 'not'
            }.get(command)
        else:
            command = {
                '+' : 'add', 
                '-' : 'sub', 
                '*' : 'call Math.multiply 2', 
                '/' : 'call Math.divide 2', 
                '&' : 'and', 
                '|' : 'or', 
                '<' : 'lt', 
                '>' : 'gt', 
                '=' : 'eq', 
                '&amp;' : 'and', 
                '&lt;' : 'lt', 
                '&gt;' : 'gt'
            }.get(command)
        self.out.write(command + '\n')

    def writeLabel(self, label):
        self.out.write('label ' + label + '\n')

    def writeGoto(self, label):
        self.out.write('goto ' + label + '\n')

    def writeIf(self, label):
        self.out.write('if-goto ' + label + '\n')

    def writeCall(self, name, nArgs):
        self.out.write('call ' + name + ' ' + str(nArgs) + '\n')

    def writeFunction(self, name, nLocals):
        self.out.write('function ' + name + ' ' + str(nLocals) + '\n')

    def writeReturn(self):
        self.out.write('return\n')

    def close(self):
        self.out.close()