class Parser:
    COMMANDS = {
            'add': 'C_ARITHMETIC',
            'sub': 'C_ARITHMETIC',
            'neg': 'C_ARITHMETIC',
            'eq': 'C_ARITHMETIC',
            'gt': 'C_ARITHMETIC',
            'lt': 'C_ARITHMETIC',
            'and': 'C_ARITHMETIC',
            'or': 'C_ARITHMETIC',
            'not': 'C_ARITHMETIC',
            'push': 'C_PUSH',
            'pop': 'C_POP',
            'label': 'C_LABEL',
            'goto': 'C_GOTO',
            'if-goto': 'C_IF',
            'function': 'C_FUNCTION',
            'call': 'C_RETURN',
            'return': 'C_CALL'
        }

    def __init__(self, fileName):
        self.file = open(fileName, 'r')
        self.findCommand()

    def hasMoreCommands(self):
        return not not self.line

    def advance(self):
        if self.hasMoreCommands():
            self.findCommand()

    def commandType(self):
        return self.COMMANDS[self.line.split(' ')[0]]

    def arg1(self):
        args = self.line.split(' ')
        if len(args) > 1:
            return self.line.split(' ')[1].strip(' \t\n\r')
        else:
            return ''

    def arg2(self):
        args = self.line.split(' ')
        if len(args) > 1:
            return self.line.split(' ')[2].strip(' \t\n\r')
        else:
            return ''

    def findCommand(self):
        line = self.file.readline()
        if not line:
            self.line = line
        else:
            self.line = self.file.readline().strip(' \t\n\r')
            if not self.line or self.line[0] == '/' and self.line[1] == '/':
                self.findCommand()
            

    
