class Symbol():
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type


class VariableSymbol(Symbol):
    def __init__(self, name, type, size=None):
        super().__init__(name, type)
        self.size = size


class SymbolTable(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        symbol = self.symbols.get(name)
        if symbol is not None:
            return symbol
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        new_scope = SymbolTable(parent=self, name=name)
        return new_scope

    def popScope(self):
        return self.parent
