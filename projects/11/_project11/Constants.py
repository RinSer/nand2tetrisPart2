# Lexical elements
KEYWORD = [
    'class', 'constructor', 'function', 'method', 'field', 'static', 'var',
    'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let',
    'do', 'if', 'else', 'while', 'return'
]
SYMBOL = [
     '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
     '&', '|', '<', '>', '=', '~'
]
# Operators
UOP = ['-', '~']

OP = [
    '+', '-', '*', '/', '&', '|', '<', '>', '=', '&amp;', '&lt;', '&gt;'
]
# Kinds of variables
KINDS = {
    'class': [ 'field', 'static' ],
    'subroutine': [ 'arg', 'var' ]
}