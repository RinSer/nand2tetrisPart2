import sys, glob, os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


def processFiles(folder):
    if '.jack' in folder:
        tokenizer = JackTokenizer(folder)
        engine = CompilationEngine(tokenizer)
        analyze(tokenizer, engine)
    else:
        if os.getcwd().split('/')[-1] != folder:
            os.chdir(folder)
        for fileName in glob.glob('*.jack'):
            tokenizer = JackTokenizer(fileName)
            engine = CompilationEngine(tokenizer)
            analyze(tokenizer, engine)


def analyze(tokenizer, engine):
    if tokenizer.getToken() == 'class':
        engine.compileClass()
    else:
        raise Exception('Jack program should be placed in a class!')
        

if __name__ == '__main__':
    if not sys.argv[1]:
        raise Exception('No file specified')
    else:
        processFiles(sys.argv[1])