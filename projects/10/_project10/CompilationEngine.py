import Constants as const

class CompilationEngine:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.out = open(tokenizer.getFileName() + '.xml', 'w')


    def compileToken(self, hasBeenCalledBy):
        hasBeenCalledBy += 1
        if self.tokenizer.hasMoreTokens():
            self.out.write(2*hasBeenCalledBy*' ' + '<' + self.tokenizer.tokenType() + '>' + ' ' + str(self.tokenizer.getToken()) + ' ' + '</' + self.tokenizer.tokenType() + '>\n')


    def compileClass(self):
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
        while self.tokenizer.getToken() != ';':
            self.compileToken(hasBeenCalledBy)
            self.tokenizer.advance()
        self.compileToken(hasBeenCalledBy)
        self.out.write(2*hasBeenCalledBy*' ' + '</classVarDec>\n')


    def compileSubroutine(self, hasBeenCalledBy):
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
        while self.tokenizer.getToken() != ')':
            self.compileToken(hasBeenCalledBy)
            self.tokenizer.advance()
        self.out.write(2*hasBeenCalledBy*' ' + '</parameterList>\n')
        self.compileToken(hasBeenCalledBy - 1)


    def compileVarDec(self, hasBeenCalledBy):
        hasBeenCalledBy += 1
        self.out.write(2*hasBeenCalledBy*' ' + '<varDec>\n')
        while self.tokenizer.getToken() != ';':
            self.compileToken(hasBeenCalledBy)
            self.tokenizer.advance()
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