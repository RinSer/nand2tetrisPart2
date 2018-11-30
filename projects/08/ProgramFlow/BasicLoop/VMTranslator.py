import sys, glob, os
from my_parser import Parser
from my_code_writer import CodeWriter
import my_consts as const


def translate(file):
    writer = CodeWriter(file)
    if '.vm' in file:
        parser = Parser(file)
    else:
        file = file if '/' == file[0] else '/' + file
        if os.getcwd().split('/')[-1] != file.split('/')[-1]:
            os.chdir(file)
        for fileName in glob.glob('*.asm'):
            if fileName != const.SYS:
                parser = Parser(fileName)
                parse(parser, writer)
        parser = Parser(const.SYS)
    parse(parser, writer)
    writer.close()
    

def parse(parser, codeWriter):
    while parser.hasMoreCommands():
        if parser.commandType() == const.ARITHMETIC:
            codeWriter.writeArithmetic(parser.command(), parser.vmCommand())
        if parser.commandType() in [ const.PUSH, const.POP ]:
            codeWriter.writePushPop(parser.commandType(), parser.arg1(), parser.arg2(), parser.vmCommand())
        if parser.commandType() == const.LABEL:
            codeWriter.writeLabel(parser.arg1(), parser.vmCommand())
        if parser.commandType() == const.GOTO:
            codeWriter.writeGoto(parser.arg1(), parser.vmCommand())
        if parser.commandType() == const.IF:
            codeWriter.writeIf(parser.arg1(), parser.vmCommand())
        if parser.commandType() == const.CALL:
            codeWriter.writeCall(parser.arg1(), parser.arg2(), parser.vmCommand())
        if parser.commandType() == const.RETURN:
            codeWriter.writeCall(parser.vmCommand)
        if parser.commandType() == const.FUNCTION:
            codeWriter.writeFunction(parser.arg1(), parser.arg2(), parser.vmCommand())
        parser.advance()


if __name__ == "__main__":
    if not sys.argv[1]:
        print('No file specified')
    else:
        translate(sys.argv[1])
