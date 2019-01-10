import Constants as const
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.className = tokenizer.getFileName()
        self.writer = VMWriter(tokenizer.getFileName())
        self.out = open(tokenizer.getFileName() + 'A.xml', 'w')


    def compileToken(self, declared = None, arg = False):
        if self.tokenizer.hasMoreTokens():
            t = self.tokenizer.tokenType()
            name = self.tokenizer.getToken()
            if t == 'identifier' and self.symbolTable.kindOf(name) != None and self.tokenizer.nextToken() != '(':
                self.out.write('<' + t + ' kind=' + self.symbolTable.kindOf(name) + ' type=' + self.symbolTable.typeOf(name) + ' idx=' + str(self.symbolTable.indexOf(name)) + '>' + ' ' + name + ' ' + '</' + t + '>\n')                    
            elif t == 'identifier' and not not declared and len(declared) > 1:
                if arg:
                    type = declared[len(declared) - 2]
                    self.out.write('<' + t + ' kind=arg type=' + type + ' idx=' + str(int(len(declared) / 2) - 1) + ' isDeclared=True>' + ' ' + name + ' ' + '</' + t + '>\n')
                elif len(declared) > 2:
                    inc = len(declared) - 3
                    self.out.write('<' + t + ' kind=' + declared[0] + ' type=' + declared[1] + ' idx=' + str(self.symbolTable.varCount(declared[0]) + inc) + ' isDeclared=True>' + ' ' + name + ' ' + '</' + t + '>\n')
            else:
                self.out.write('<' + t + '>' + ' ' + str(name) + ' ' + '</' + t + '>\n')


    def compileClass(self):
        self.symbolTable = SymbolTable()
        #self.out.write('<class>\n')
        while self.tokenizer.hasMoreTokens():
            if self.tokenizer.getToken() == 'static' or self.tokenizer.getToken() == 'field':
                self.compileClassVarDec()
            elif self.tokenizer.getToken() in ['constructor', 'function', 'method']:
                self.compileSubroutine()
            #else:
                #self.compileToken(hasBeenCalledBy)
            self.tokenizer.advance()
        #self.out.write('</class>\n')
        self.out.close()
        self.writer.close()


    def compileClassVarDec(self):
        #self.out.write('<classVarDec>\n')
        variable = []
        while self.tokenizer.getToken() != ';':
            if self.tokenizer.getToken() != ',':
                variable.append(self.tokenizer.getToken())
            #self.compileToken(variable)
            self.tokenizer.advance()
        self.symbolTable.define(variable[2:], variable[1], variable[0])
        #self.compileToken()
        #self.out.write('</classVarDec>\n')


    def compileSubroutine(self):
        self.symbolTable.startSubroutine()
        #self.out.write('<subroutineDec>\n')
        functionName = None
        getType = False
        getName = False
        while self.tokenizer.getToken() != '{':
            if self.tokenizer.getToken() == '(':
                self.compileParameterList()
            elif self.tokenizer.getToken() in ['constructor', 'method', 'function']:
                getType = True
            elif getType:
                getName = True
                getType = False
            elif getName:
                functionName = self.tokenizer.getToken()
                getName = False
            #else:
                #self.compileToken()
            self.tokenizer.advance()
        #self.out.write('<subroutineBody>\n')
        #self.compileToken() # {
        self.tokenizer.advance()
        numLocals = 0
        while self.tokenizer.getToken() == 'var':
            numLocals += self.compileVarDec()
            self.tokenizer.advance()
        self.writer.writeFunction(self.className + '.' + functionName, numLocals)
        self.compileStatements()
        self.tokenizer.advance()
        #self.compileToken() # }
        #self.out.write('</subroutineBody>\n')
        #self.out.write('</subroutineDec>\n')


    def compileParameterList(self):
        #self.compileToken()
        self.tokenizer.advance()
        #self.out.write('<parameterList>\n')
        variables = []
        while self.tokenizer.getToken() != ')':
            if self.tokenizer.getToken() != ',':
                variables.append(self.tokenizer.getToken())
            #self.compileToken(variables, True)
            self.tokenizer.advance()
        idx = 0
        for variable in variables:
            if idx % 2 != 0:
                self.symbolTable.define([variable], variables[idx-1], 'arg')
            idx += 1
        #self.out.write('</parameterList>\n')
        #self.compileToken()


    def compileVarDec(self):
        #self.out.write('<varDec>\n')
        variable = []
        while self.tokenizer.getToken() != ';':
            if self.tokenizer.getToken() != ',':
                variable.append(self.tokenizer.getToken())
            #self.compileToken(variable)
            self.tokenizer.advance()
        self.symbolTable.define(variable[2:], variable[1], variable[0])
        #self.compileToken()
        #self.out.write('</varDec>\n')
        return len(variable[2:])
        

    def compileStatements(self):
        #self.out.write('<statements>\n')
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
        #self.out.write('</statements>\n')


    def compileLet(self):
        self.out.write('<letStatement>\n')
        self.compileToken() # let
        self.tokenizer.advance()
        self.compileToken() # varName
        self.tokenizer.advance()
        if self.tokenizer.getToken() == '[':
            self.compileToken() # [
            self.tokenizer.advance()
            self.compileExpression() # expression
            self.compileToken() # ]
            self.tokenizer.advance()
        self.compileToken() # =
        self.tokenizer.advance()
        self.compileExpression() # expression
        self.compileToken() # ;
        self.tokenizer.advance()
        self.out.write('</letStatement>\n')


    def compileIf(self):
        self.out.write('<ifStatement>\n')
        self.compileToken() # if
        self.tokenizer.advance()
        self.compileToken() # (
        self.tokenizer.advance()
        self.compileExpression() # expression
        self.compileToken() # )
        self.tokenizer.advance()
        self.compileToken() # {
        self.tokenizer.advance()
        self.compileStatements() # statements
        self.compileToken() # }
        self.tokenizer.advance()
        if self.tokenizer.getToken() == 'else':
            self.compileToken() # else
            self.tokenizer.advance()
            self.compileToken() # {
            self.tokenizer.advance()
            self.compileStatements() # statements
            self.compileToken() # }
            self.tokenizer.advance()
        self.out.write('</ifStatement>\n')


    def compileWhile(self):
        self.out.write('<whileStatement>\n')
        self.compileToken() # while
        self.tokenizer.advance()
        self.compileToken() # (
        self.tokenizer.advance()
        self.compileExpression() # expression
        self.compileToken() # )
        self.tokenizer.advance()
        self.compileToken() # {
        self.tokenizer.advance()
        self.compileStatements() # statements
        self.compileToken() # }
        self.tokenizer.advance()
        self.out.write('</whileStatement>\n')


    def compileDo(self):
        self.out.write('<doStatement>\n')
        while self.tokenizer.getToken() != '(':
            self.compileToken() # do [(className | varName) .]? subroutineName
            self.tokenizer.advance()
        self.compileToken() # (
        self.tokenizer.advance()
        self.compileExpressionList() # expressionList
        self.compileToken() # )
        self.tokenizer.advance()
        self.compileToken() # ;
        self.tokenizer.advance()
        self.out.write('</doStatement>\n')


    def compileReturn(self):
        self.out.write('<returnStatement>\n')
        self.compileToken() # return
        self.tokenizer.advance()
        if self.tokenizer.getToken() == ';':
            self.compileToken() # ;
        else:
            self.compileExpression() # expression?
            self.compileToken() # ;
        self.out.write('</returnStatement>\n')


    def compileExpression(self):
        self.out.write('<expression>\n')
        expLen = 0
        while self.tokenizer.getToken() not in [';', ')', ']', ',']:
            if self.tokenizer.getToken() in const.UOP and expLen == 0:
                self.compileTerm()
            elif self.tokenizer.getToken() in const.OP:
                self.compileToken()
                self.tokenizer.advance()
            else:
                self.compileTerm()
            expLen += 1
        self.out.write('</expression>\n')


    def compileTerm(self):
        self.out.write('<term>\n')
        if self.tokenizer.getToken() == '(':
            self.compileToken() # (
            self.tokenizer.advance()
            self.compileExpression() # expression
            self.compileToken() # )
            self.tokenizer.advance()
            self.out.write('</term>\n')
            return
        if self.tokenizer.getToken() in const.UOP:
            self.compileToken() # UOP
            self.tokenizer.advance()
            self.compileTerm()
        if self.tokenizer.getToken() in [';', ')', ']', ',']:
            self.out.write('</term>\n')
            return
        if self.tokenizer.getToken() not in const.OP:
            self.compileToken() # varName, etc.
            self.tokenizer.advance()
        if self.tokenizer.getToken() == '[':
            self.compileToken() # [
            self.tokenizer.advance()
            self.compileExpression() # expression
            self.compileToken() # ]
            self.tokenizer.advance()
        if self.tokenizer.getToken() == '.':
            self.compileToken() # .
            self.tokenizer.advance()
            self.compileToken() # identifier
            self.tokenizer.advance()
        if self.tokenizer.getToken() == '(':
            self.compileToken() # (
            self.tokenizer.advance()
            self.compileExpressionList() # expressionList
            self.compileToken() # )
            self.tokenizer.advance()
        self.out.write('</term>\n')


    def compileExpressionList(self):
        self.out.write('<expressionList>\n')
        while self.tokenizer.getToken() != ')':
            if self.tokenizer.getToken() == ',':
                self.compileToken() # ,?
                self.tokenizer.advance()
            else:
                self.compileExpression()
        self.out.write('</expressionList>\n')