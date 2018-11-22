import sys
from my_parser import Parser

def translate(file):
    parser = Parser(file)
    while parser.hasMoreCommands():
        print(parser.commandType())
        print(parser.arg1())
        print(parser.arg2())
        parser.advance()

if __name__ == "__main__":
    if not sys.argv[1]:
        print('No file specified')
    else:
        translate(sys.argv[1])
