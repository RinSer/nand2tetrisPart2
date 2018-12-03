import my_consts as const

class Parser:
    COMMANDS = {
            const.ADD: const.ARITHMETIC,
            const.SUB: const.ARITHMETIC,
            const.NEG: const.ARITHMETIC,
            const.EQ: const.ARITHMETIC,
            const.GT: const.ARITHMETIC,
            const.LT: const.ARITHMETIC,
            const.AND: const.ARITHMETIC,
            const.OR: const.ARITHMETIC,
            const.NOT: const.ARITHMETIC,
            'push': const.PUSH,
            'pop': const.POP,
            'label': const.LABEL,
            'goto': const.GOTO,
            'if-goto': const.IF,
            'function': const.FUNCTION,
            'call': const.CALL,
            'return': const.RETURN
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

    def command(self):
        return self.line.split(' ')[0].strip(' \t\n\r')

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

    def vmCommand(self):
        return self.line

    def findCommand(self):
        line = self.file.readline()
        if not line:
            self.line = line
            self.file.close()
        else:
            self.line = line.strip(' \t\n\r')
            if not self.line or self.line[0] == '/' and self.line[1] == '/':
                self.findCommand()
