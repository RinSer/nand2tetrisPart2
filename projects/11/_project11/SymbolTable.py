import Constants as const

'''
SymbolTable consists of two dictionaries:
1) for class variables
2) for subroutine variables
Each dictionary has two dictionaries for each relevant kind.
Each kind dictionary schema: (key: name => tuple(type, index))
'''
class SymbolTable:
    def __init__(self):
        self.classTable = {
            'field': dict(),
            'static': dict()
        }
        self.startSubroutine()

    def startSubroutine(self):
        self.subTable = {
            'arg': dict(),
            'var': dict()
        }

    def define(self, names, type, kind):
        for name in names:
            if kind in const.KINDS['class']:
                self.classTable[kind].update({name : (type, self.varCount(kind))})
            if kind in const.KINDS['subroutine']:
                self.subTable[kind].update({name : (type, self.varCount(kind))})

    def varCount(self, kind):
        if kind in const.KINDS['class']:
            return len(self.classTable[kind])
        if kind in const.KINDS['subroutine']:
            return len(self.subTable[kind])

    def kindOf(self, name):
        if name in self.subTable['arg'].keys():
            return 'arg'
        if name in self.subTable['var'].keys():
            return 'var'
        if name in self.classTable['field'].keys():
            return 'field'
        if name in self.classTable['static'].keys():
            return 'static'
        return None

    def typeOf(self, name):
        kind = self.kindOf(name)
        if kind in const.KINDS['class']:
            return self.classTable[kind][name][0]
        if kind in const.KINDS['subroutine']:
            return self.subTable[kind][name][0]

    def indexOf(self, name):
        kind = self.kindOf(name)
        if kind in const.KINDS['class']:
            return self.classTable[kind][name][1]
        if kind in const.KINDS['subroutine']:
            return self.subTable[kind][name][1]