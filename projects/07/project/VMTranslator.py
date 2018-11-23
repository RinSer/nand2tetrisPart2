import sys
from my_parser import Parser
from my_code_writer import CodeWriter
import my_consts as const

def translate(file):
    parser = Parser(file)
    codeWriter = CodeWriter(file)
    while parser.hasMoreCommands():
        if parser.commandType() == const.ARITHMETIC:
            codeWriter.writeArithmetic(parser.command(), parser.vmCommand())
        if parser.commandType() in [ const.PUSH, const.POP ]:
            codeWriter.writePushPop(parser.commandType(), parser.arg1(), parser.arg2(), parser.vmCommand())
        parser.advance()
    codeWriter.close()

if __name__ == "__main__":
    if not sys.argv[1]:
        print('No file specified')
    else:
        translate(sys.argv[1])
