import Constants as const
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:
    def __init__(self, tokenizer, classDict):
        self.tokenizer = tokenizer
        self.className = tokenizer.getFileName()
        self.resetLabelCounters()
        self.writer = VMWriter(tokenizer.getFileName())


    def resetLabelCounters(self):
        self.ifLabelCounter = 0
        self.whileLabelCounter = 0


    def compileClass(self):
        self.symbolTable = SymbolTable()
        while self.tokenizer.hasMoreTokens():
            if self.tokenizer.getToken() == 'static' or self.tokenizer.getToken() == 'field':
                self.compileClassVarDec()
            elif self.tokenizer.getToken() in const.SUBS:
                self.compileSubroutine()
            if not self.tokenizer.getToken() in const.SUBS:
                self.tokenizer.advance()
        self.writer.close()


    def compileClassVarDec(self):
        variable = []
        while self.tokenizer.getToken() != ';':
            if self.tokenizer.getToken() != ',':
                variable.append(self.tokenizer.getToken())
            self.tokenizer.advance()
        self.symbolTable.define(variable[2:], variable[1], variable[0])


    def compileSubroutine(self):
        self.symbolTable.startSubroutine()
        functionName = None
        getType = False
        getName = False
        while self.tokenizer.getToken() != '{':
            if self.tokenizer.getToken() == '(':
                self.compileParameterList()
            elif self.tokenizer.getToken() in const.SUBS:
                getType = True
            elif getType:
                getName = True
                getType = False
            elif getName:
                functionName = self.tokenizer.getToken()
                getName = False
            self.tokenizer.advance()
        self.tokenizer.advance() # {
        numLocals = 0
        while self.tokenizer.getToken() == 'var':
            numLocals += self.compileVarDec()
            self.tokenizer.advance()
        self.writer.writeFunction(self.className + '.' + functionName, numLocals)
        self.resetLabelCounters()
        self.compileStatements()
        if self.tokenizer.getToken() == '}':
            self.tokenizer.advance() # }


    def compileParameterList(self):
        self.tokenizer.advance()
        variables = []
        while self.tokenizer.getToken() != ')':
            if self.tokenizer.getToken() != ',':
                variables.append(self.tokenizer.getToken())
            self.tokenizer.advance()
        idx = 0
        for variable in variables:
            if idx % 2 != 0:
                self.symbolTable.define([variable], variables[idx-1], 'arg')
            idx += 1


    def compileVarDec(self):
        variable = []
        while self.tokenizer.getToken() != ';':
            if self.tokenizer.getToken() != ',':
                variable.append(self.tokenizer.getToken())
            self.tokenizer.advance()
        self.symbolTable.define(variable[2:], variable[1], variable[0])
        return len(variable[2:])
        

    def compileStatements(self):
        while self.tokenizer.getToken() in ['let', 'if', 'while', 'do', 'return']:
            if self.tokenizer.getToken() == 'let':
                self.compileLet()
            if self.tokenizer.getToken() == 'if':
                self.compileIf()
            if self.tokenizer.getToken() == 'while':
                self.compileWhile()
            if self.tokenizer.getToken() == 'do':
                self.compileDo()
            if self.tokenizer.getToken() == 'return':
                self.compileReturn()


    def compileLet(self):
        self.tokenizer.advance() # let
        assignee = self.tokenizer.getToken()
        self.tokenizer.advance() # varName
        if self.tokenizer.getToken() == '[':
            self.tokenizer.advance() # [
            self.compileExpression() # expression
            self.tokenizer.advance() # ]
        self.tokenizer.advance() # =
        self.compileExpression() # expression
        if not self.symbolTable.kindOf(assignee):
            raise Exception('Undeclared identifier assignment ' + assignee)
        else:
            self.writer.writePop(self.symbolTable.kindOf(assignee), self.symbolTable.indexOf(assignee))


    def getLabel(self, labelName, increment = False):
        label = labelName
        if 'WHILE' in labelName:
            label += str(self.whileLabelCounter)
            if increment:
                self.whileLabelCounter += 1
        if 'IF' in labelName:
            label += str(self.ifLabelCounter)
            if increment:
                self.ifLabelCounter += 1
        return label


    def compileIf(self):
        firstLabel = self.getLabel('IF_TRUE')
        secondLabel = self.getLabel('IF_FALSE')
        endLabel = self.getLabel('IF_END', True)
        self.tokenizer.advance() # if
        self.tokenizer.advance() # (
        self.compileExpression() # expression
        self.tokenizer.advance() # )
        self.writer.writeIf(firstLabel)
        self.writer.writeGoto(secondLabel)
        self.writer.writeLabel(firstLabel)
        self.tokenizer.advance() # {
        self.compileStatements() # statements
        self.tokenizer.advance() # }
        if self.tokenizer.getToken() == 'else':
            self.writer.writeGoto(endLabel)
            self.writer.writeLabel(secondLabel)
            self.tokenizer.advance() # else
            self.tokenizer.advance() # {
            self.compileStatements() # statements
            self.tokenizer.advance() # }
            self.writer.writeLabel(endLabel)
        else:
            self.writer.writeLabel(secondLabel)


    def compileWhile(self):
        firstLabel = self.getLabel('WHILE_EXP')
        secondLabel = self.getLabel('WHILE_END', True)
        self.writer.writeLabel(firstLabel)
        self.tokenizer.advance() # while
        self.tokenizer.advance() # (
        self.compileExpression() # expression
        self.tokenizer.advance() # )
        self.writer.writeArithmetic('~', True) # negating the expression
        self.writer.writeIf(secondLabel)
        self.tokenizer.advance() # {
        self.compileStatements() # statements
        self.tokenizer.advance() # }
        self.writer.writeGoto(firstLabel)
        self.writer.writeLabel(secondLabel)


    def compileDo(self):
        self.tokenizer.advance() # do
        functionName = ''
        if self.tokenizer.nextToken() == '.':
            if not self.symbolTable.typeOf(self.tokenizer.getToken()):
                functionName = self.tokenizer.getToken()
            else:
                functionName = self.symbolTable.typeOf(self.tokenizer.getToken())
            self.tokenizer.advance() # (className | varName)
            functionName += '.'
            self.tokenizer.advance() # .
        functionName += self.tokenizer.getToken()
        self.tokenizer.advance() # subroutineName
        self.tokenizer.advance() # (
        numArgs = self.compileExpressionList() # expressionList
        self.tokenizer.advance() # )
        self.tokenizer.advance() # ;
        self.writer.writeCall(functionName, numArgs)
        self.writer.writePop('temp', 0)


    def compileReturn(self):
        if self.tokenizer.nextToken() == ';':
            self.writer.writePush('constant', 0)
        self.tokenizer.advance() # return
        if self.tokenizer.getToken() != ';':
            self.compileExpression() # expression?
        self.writer.writeReturn()


    def compileExpression(self):
        op = None
        expLen = 0
        while self.tokenizer.getToken() not in [';', ')', ']', ',']:
            if self.tokenizer.getToken() in const.UOP and expLen == 0:
                self.compileTerm()
            elif self.tokenizer.getToken() in const.OP:
                op = self.tokenizer.getToken()
                self.tokenizer.advance()
            else:
                self.compileTerm()
            expLen += 1
        if not not op:
            self.writer.writeArithmetic(op)
        if self.tokenizer.getToken() == ';':
            self.tokenizer.advance() # ;


    def compileTerm(self):
        if self.tokenizer.getToken() == '(':
            self.tokenizer.advance() # (
            self.compileExpression() # expression
            self.tokenizer.advance() # )
            return
        uop = None
        if self.tokenizer.getToken() in const.UOP:
            uop = self.tokenizer.getToken()
            self.tokenizer.advance() # UOP
            self.compileTerm()
            if not not uop:
                self.writer.writeArithmetic(uop, True)
        if self.tokenizer.getToken() in [';', ')', ']', ',']:
            return
        if self.tokenizer.getToken() not in const.OP and self.tokenizer.nextToken() not in ['[', '.', '(']:
            if not not self.symbolTable.kindOf(self.tokenizer.getToken()):
                self.writer.writePush(self.symbolTable.kindOf(self.tokenizer.getToken()), self.symbolTable.indexOf(self.tokenizer.getToken()))
            else:
                self.writer.writePush('constant', self.tokenizer.getToken())
            self.tokenizer.advance() # varName, etc.
        elif self.tokenizer.nextToken() in ['[', '.', '(']:
            functionName = ''
            if not self.symbolTable.typeOf(self.tokenizer.getToken()):
                functionName += self.tokenizer.getToken()
            else:
                functionName += self.symbolTable.typeOf(self.tokenizer.getToken())
            self.tokenizer.advance() # varName, etc.
            if self.tokenizer.getToken() == '[':
                self.tokenizer.advance() # [
                self.compileExpression() # expression
                self.tokenizer.advance() # ]
            if self.tokenizer.getToken() == '.':
                self.tokenizer.advance() # .
                functionName += '.' + self.tokenizer.getToken()
                self.tokenizer.advance() # identifier
            numArgs = 0
            if self.tokenizer.getToken() == '(':
                self.tokenizer.advance() # (
                numArgs = self.compileExpressionList() # expressionList
                self.tokenizer.advance() # )
                self.writer.writeCall(functionName, numArgs)


    def compileExpressionList(self):
        count = 0
        while self.tokenizer.getToken() != ')':
            if self.tokenizer.getToken() == ',':
                self.tokenizer.advance() # ,?
            else:
                self.compileExpression()
                count += 1
        return count