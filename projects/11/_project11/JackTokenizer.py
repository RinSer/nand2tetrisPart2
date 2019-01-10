import re
import Constants as const

class JackTokenizer:
    def __init__(self, fileName):
        # read file, remove comments and white spaces
        self.file = open(fileName, 'r')
        self.content = re.sub(r'\n+|\r+|\/\/.*', '', self.file.read())
        self.file.close()
        self.content = re.sub(r'\/\*.*?\*\/', '', self.content)
        self.content = re.sub(r'\s+', ' ', self.content)
        self.fileName = fileName.split('.')[0]
        self.token = ''
        self.advance()

    def getFileName(self):
        return self.fileName

    def hasMoreTokens(self):
        return not not self.token

    def nextToken(self):
        if len(self.content) > 0:
            idx = 0
            token = self.content[idx]
            if token == ' ':
                idx += 1
                if idx < len(self.content):
                    token = self.content[idx]
            if token != ' ':
                while idx != (len(self.content) - 1) and token not in const.SYMBOL and token not in const.KEYWORD and self.content[idx + 1] not in const.SYMBOL and (self.content[idx + 1] != ' ' or token[0] == '"'):
                    idx += 1
                    token += self.content[idx]
                return token
        return None

    def advance(self):
        if len(self.content) > 0:
            idx = 0
            self.token = self.content[idx]
            if self.token != ' ':
                while idx != (len(self.content) - 1) and self.token not in const.SYMBOL and self.token not in const.KEYWORD and self.content[idx + 1] not in const.SYMBOL and (self.content[idx + 1] != ' ' or self.token[0] == '"'):
                    idx += 1
                    self.token += self.content[idx]
            if idx == len(self.content):
                self.content = ''
            else:
                self.content = self.content[(idx + 1):]
            if self.token == ' ':
                self.advance()
        else:
            self.token = None

    def tokenType(self):
        if self.token in const.KEYWORD:
            return 'keyword'
        if self.token in const.SYMBOL:
            return 'symbol'
        if not not re.match(r'\d+', self.token):
            return 'integerConstant'
        if not not re.match(r'\w+', self.token):
            return 'identifier'
        if not not re.match(r'\".*\"', self.token):
            return 'stringConstant'

    def getToken(self):
        if not self.token:
            return None
        if self.token in const.KEYWORD:
            return self.keyWord()
        if self.token in const.SYMBOL:
            return self.symbol()
        if not not re.match(r'\d+', self.token):
            return self.intVal()
        if not not re.match(r'\w+', self.token):
            return self.identifier()
        if not not re.match(r'\".*\"', self.token):
            return self.stringVal()

    def keyWord(self):
        return self.token

    def symbol(self):
        if self.token == '<':
            return '&lt;'
        if self.token == '>':
            return '&gt;'
        if self.token == '&':
            return '&amp;'
        return self.token

    def identifier(self):
        return self.token

    def intVal(self):
        return int(self.token)

    def stringVal(self):
        return re.sub(r'\"', '', self.token)