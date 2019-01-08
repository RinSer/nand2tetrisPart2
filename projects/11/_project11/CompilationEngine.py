import Constants as const
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.out = open(tokenizer.getFileName() + 'A.xml', 'w')


    def compileToken(self, hasBeenCalledBy, declared = None, arg = False):
        hasBeenCalledBy += 1
        if self.tokenizer.hasMoreTokens():
            t = self.tokenizer.tokenType()
            name = self.tokenizer.getToken()
            if t == 'identifier' and self.symbolTable.kindOf(name) != None:
                self.out.write(2*hasBeenCalledBy*' ' + '<' + t + ' kind=' + self.symbolTable.kindOf(name) + ' type=' + self.symbolTable.typeOf(name) + ' idx=' + str(self.symbolTable.indexOf(name)) + '>' + ' ' + name + ' ' + '</' + t + '>\n')                    
            elif t == 'identifier' and not not declared and len(declared) > 1:
                if arg:
                    type = declared[len(declared) - 2]
                    self.out.write(2*hasBeenCalledBy*' ' + '<' + t + ' kind=arg type=' + type + ' idx=' + str(int(len(declared) / 2)) + ' isDeclared=True>' + ' ' + name + ' ' + '</' + t + '>\n')
                elif len(declared) > 2:
                    inc = len(declared) - 3
                    self.out.write(2*hasBeenCalledBy*' ' + '<' + t + ' kind=' + declared[0] + ' type=' + declared[1] + ' idx=' + str(self.symbolTable.varCount(declared[0]) + inc) + ' isDeclared=True>' + ' ' + name + ' ' + '</' + t + '>\n')
            else:
                self.out.write(2*hasBeenCalledBy*' ' + '<' + t + '>' + ' ' + str(name) + ' ' + '</' + t + '>\n')


    def compileClass(self):
        self.symbolTable = SymbolTable()
        hasBeenCalledBy = 0
        self.out.write('<class>\n')
        while self.tokenizer.hasMoreTokens():
            if self.tokenizer.getToken() == 'static' or self.tokenizer.getToken() == 'field':
                self.compileClassVarDec(hasBeenCalledBy)
            elif self.tokenizer.getToken() in ['constructor', 'function', 'method']:
                self.compileSubroutine(hasBeenCalledBy)
            else:
                self.compileToken(hasBeenCalledBy)
            self.tokenizer.advance()
        self.out.write('</class>\n')
        self.out.close()


    def compileClassVarDec(self, hasBeenCalledBy):
        hasBeenCalledBy += 1
        self.out.write(2*hasBeenCalledBy*' ' + '<classVarDec>\n')
        variable = []
        while self.tokenizer.getToken() != ';':
            if self.tokenizer.getToken() != ',':
                variable.append(self.tokenizer.getToken())
            self.compileToken(hasBeenCalledBy, variable)
            self.tokenizer.advance()
        self.symbolTable.define(variable[2:], variable[1], variable[0])
        self.compileToken(hasBeenCalledBy)
        self.out.write(2*hasBeenCalledBy*' ' + '</classVarDec>\n')


    def compileSubroutine(self, hasBeenCalledBy):
        self.symbolTable.startSubroutine()
        hasBeenCalledBy += 1
        self.out.write(2*hasBeenCalledBy*' ' + '<subroutineDec>\n')
        while self.tokenizer.getToken() != '{':
            if self.tokenizer.getToken() == '(':
                self.compileParameterList(hasBeenCalledBy)
            else:
                self.compileToken(hasBeenCalledBy)
            self.tokenizer.advance()
        self.out.write(2*(hasBeenCalledBy+1)*' ' + '<subroutineBody>\n')
        self.compileToken(hasBeenCalledBy + 1) # {
        self.tokenizer.advance()
        while self.tokenizer.getToken() == 'var':
            self.compileVarDec(hasBeenCalledBy + 1)
            self.tokenizer.advance()
        self.compileStatements(hasBeenCalledBy + 1)
        self.tokenizer.advance()
        self.compileToken(hasBeenCalledBy + 1) # }
        self.out.write(4*hasBeenCalledBy*' ' + '</subroutineBody>\n')
        self.out.write(2*hasBeenCalledBy*' ' + '</subroutineDec>\n')


    def compileParameterList(self, hasBeenCalledBy):
        hasBeenCalledBy += 1
        self.compileToken(hasBeenCalledBy - 1)
        self.tokenizer.advance()
        self.out.write(2*hasBeenCalledBy*' ' + '<parameterList>\n')
        variables = []
        while self.tokenizer.getToken() != ')':
            if self.tokenizer.getToken() != ',':
                variables.append(self.tokenizer.getToken())
            self.compileToken(hasBeenCalledBy, variables, True)
            self.tokenizer.advance()
        idx = 0
        for variable in variables:
            if idx % 2 != 0:
                self.symbolTable.define([variable], variables[idx-1], 'arg')
            idx += 1
        self.out.write(2*hasBeenCalledBy*' ' + '</parameterList>\n')
        self.compileToken(hasBeenCalledBy - 1)


    def compileVarDec(self, hasBeenCalledBy):
        hasBeenCalledBy += 1
        self.out.write(2*hasBeenCalledBy*' ' + '<varDec>\n')
        variable = []
        while self.tokenizer.getToken() != ';':
            if self.tokenizer.getToken() != ',':
                variable.append(self.tokenizer.getToken())
            self.compileToken(hasBeenCalledBy, variable)
            self.tokenizer.advance()
        self.symbolTable.define(variable[2:], variable[1], variable[0])
        self.compileToken(hasBeenCalledBy)
        self.out.write(2*hasBeenCalledBy*' ' + '</varDec>\n')
        

    def compileStatements(self, hasBeenCalledBy):
        hasBeenCalledBy += 1
        self.out.write(2*hasBeenCalledBy*' ' + '<statements>\n')
        while self.tokenizer.getToken() in ['let', 'if', 'while', 'do', 'return']:
            if self.tokenizer.getToken() == 'let':
                self.compileLet(hasBeenCalledBy + 1)
            if self.tokenizer.getToken() == 'if':
                self.compileIf(hasBeenCalledBy + 1)
            if self.tokenizer.getToken() == 'while':
                self.compileWhile(hasBeenCalledBy + 1)
            if self.tokenizer.getToken() == 'do':
                self.compileDo(hasBeenCalledBy + 1)
            if self.tokenizer.getToken() == 'return':
                self.compileReturn(hasBeenCalledBy + 1)
        self.out.write(2*hasBeenCalledBy*' ' + '</statements>\n')


    def compileLet(self, hasBeenCalledBy):
        self.out.write(2*hasBeenCalledBy*' ' + '<letStatement>\n')
        self.compileToken(hasBeenCalledBy) # let
        self.tokenizer.advance()
        self.compileToken(hasBeenCalledBy) # varName
        self.tokenizer.advance()
        if self.tokenizer.getToken() == '[':
            self.compileToken(hasBeenCalledBy) # [
            self.tokenizer.advance()
            self.compileExpression(hasBeenCalledBy + 1) # expression
            self.compileToken(hasBeenCalledBy) # ]
            self.tokenizer.advance()
        self.compileToken(hasBeenCalledBy) # =
        self.tokenizer.advance()
        self.compileExpression(hasBeenCalledBy + 1) # expression
        self.compileToken(hasBeenCalledBy) # ;
        self.tokenizer.advance()
        self.out.write(2*hasBeenCalledBy*' ' + '</letStatement>\n')


    def compileIf(self, hasBeenCalledBy):
        self.out.write(2*hasBeenCalledBy*' ' + '<ifStatement>\n')
        self.compileToken(hasBeenCalledBy) # if
        self.tokenizer.advance()
        self.compileToken(hasBeenCalledBy) # (
        self.tokenizer.advance()
        self.compileExpression(hasBeenCalledBy + 1) # expression
        self.compileToken(hasBeenCalledBy) # )
        self.tokenizer.advance()
        self.compileToken(hasBeenCalledBy) # {
        self.tokenizer.advance()
        self.compileStatements(hasBeenCalledBy) # statements
        self.compileToken(hasBeenCalledBy) # }
        self.tokenizer.advance()
        if self.tokenizer.getToken() == 'else':
            self.compileToken(hasBeenCalledBy) # else
            self.tokenizer.advance()
            self.compileToken(hasBeenCalledBy) # {
            self.tokenizer.advance()
            self.compileStatements(hasBeenCalledBy) # statements
            self.compileToken(hasBeenCalledBy) # }
            self.tokenizer.advance()
        self.out.write(2*hasBeenCalledBy*' ' + '</ifStatement>\n')


    def compileWhile(self, hasBeenCalledBy):
        self.out.write(2*hasBeenCalledBy*' ' + '<whileStatement>\n')
        self.compileToken(hasBeenCalledBy + 1) # while
        self.tokenizer.advance()
        self.compileToken(hasBeenCalledBy + 1) # (
        self.tokenizer.advance()
        self.compileExpression(hasBeenCalledBy + 1) # expression
        self.compileToken(hasBeenCalledBy + 1) # )
        self.tokenizer.advance()
        self.compileToken(hasBeenCalledBy + 1) # {
        self.tokenizer.advance()
        self.compileStatements(hasBeenCalledBy + 1) # statements
        self.compileToken(hasBeenCalledBy + 1) # }
        self.tokenizer.advance()
        self.out.write(2*hasBeenCalledBy*' ' + '</whileStatement>\n')


    def compileDo(self, hasBeenCalledBy):
        self.out.write(2*hasBeenCalledBy*' ' + '<doStatement>\n')
        while self.tokenizer.getToken() != '(':
            self.compileToken(hasBeenCalledBy) # do [(className | varName) .]? subroutineName
            self.tokenizer.advance()
        self.compileToken(hasBeenCalledBy) # (
        self.tokenizer.advance()
        self.compileExpressionList(hasBeenCalledBy) # expressionList
        self.compileToken(hasBeenCalledBy) # )
        self.tokenizer.advance()
        self.compileToken(hasBeenCalledBy) # ;
        self.tokenizer.advance()
        self.out.write(2*hasBeenCalledBy*' ' + '</doStatement>\n')


    def compileReturn(self, hasBeenCalledBy):
        self.out.write(2*hasBeenCalledBy*' ' + '<returnStatement>\n')
        self.compileToken(hasBeenCalledBy) # return
        self.tokenizer.advance()
        if self.tokenizer.getToken() == ';':
            self.compileToken(hasBeenCalledBy + 1) # ;
        else:
            self.compileExpression(hasBeenCalledBy + 1) # expression?
            self.compileToken(hasBeenCalledBy + 1) # ;
        self.out.write(2*hasBeenCalledBy*' ' + '</returnStatement>\n')


    def compileExpression(self, hasBeenCalledBy):
        self.out.write(2*hasBeenCalledBy*' ' + '<expression>\n')
        expLen = 0
        while self.tokenizer.getToken() not in [';', ')', ']', ',']:
            if self.tokenizer.getToken() in const.UOP and expLen == 0:
                self.compileTerm(hasBeenCalledBy + 1)
            elif self.tokenizer.getToken() in const.OP:
                self.compileToken(hasBeenCalledBy)
                self.tokenizer.advance()
            else:
                self.compileTerm(hasBeenCalledBy + 1)
            expLen += 1
        self.out.write(2*hasBeenCalledBy*' ' + '</expression>\n')


    def compileTerm(self, hasBeenCalledBy):
        self.out.write(2*hasBeenCalledBy*' ' + '<term>\n')
        if self.tokenizer.getToken() == '(':
            self.compileToken(hasBeenCalledBy) # (
            self.tokenizer.advance()
            self.compileExpression(hasBeenCalledBy + 1) # expression
            self.compileToken(hasBeenCalledBy) # )
            self.tokenizer.advance()
            self.out.write(2*hasBeenCalledBy*' ' + '</term>\n')
            return
        if self.tokenizer.getToken() in const.UOP:
            self.compileToken(hasBeenCalledBy) # UOP
            self.tokenizer.advance()
            self.compileTerm(hasBeenCalledBy + 1)
        if self.tokenizer.getToken() in [';', ')', ']', ',']:
            self.out.write(2*hasBeenCalledBy*' ' + '</term>\n')
            return
        if self.tokenizer.getToken() not in const.OP:
            self.compileToken(hasBeenCalledBy) # varName, etc.
            self.tokenizer.advance()
        if self.tokenizer.getToken() == '[':
            self.compileToken(hasBeenCalledBy) # [
            self.tokenizer.advance()
            self.compileExpression(hasBeenCalledBy + 1) # expression
            self.compileToken(hasBeenCalledBy) # ]
            self.tokenizer.advance()
        if self.tokenizer.getToken() == '.':
            self.compileToken(hasBeenCalledBy) # .
            self.tokenizer.advance()
            self.compileToken(hasBeenCalledBy) # identifier
            self.tokenizer.advance()
        if self.tokenizer.getToken() == '(':
            self.compileToken(hasBeenCalledBy) # (
            self.tokenizer.advance()
            self.compileExpressionList(hasBeenCalledBy) # expressionList
            self.compileToken(hasBeenCalledBy) # )
            self.tokenizer.advance()
        self.out.write(2*hasBeenCalledBy*' ' + '</term>\n')


    def compileExpressionList(self, hasBeenCalledBy):
        self.out.write(2*hasBeenCalledBy*' ' + '<expressionList>\n')
        while self.tokenizer.getToken() != ')':
            if self.tokenizer.getToken() == ',':
                self.compileToken(hasBeenCalledBy) # ,?
                self.tokenizer.advance()
            else:
                self.compileExpression(hasBeenCalledBy + 1)
        self.out.write(2*hasBeenCalledBy*' ' + '</expressionList>\n')