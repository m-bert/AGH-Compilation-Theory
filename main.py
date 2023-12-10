from MyParser import MyParser
from MyScanner import MyLexer
from TypeChecker import TypeChecker
from Interpreter import Interpreter


if __name__ == '__main__':

    with open("./examples/z5/fibonacci.m", "r") as f:
        data = f.read()
        
        lexer = MyLexer()
        parser = MyParser()
        typeChecker = TypeChecker()
        interpreter = Interpreter()

        ast = parser.parse(lexer.tokenize(data))

        typeChecker.visit(ast)
        interpreter.visit(ast)
