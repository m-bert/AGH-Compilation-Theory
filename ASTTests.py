from MyScanner import MyLexer
from MyParser import MyParser
from TreePrinter import TreePrinter

if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    tp = TreePrinter()

    print("##### [TEST 1] #####")
    with open("examples/z3/ex1.txt") as file:
        data = file.read()
        ast = parser.parse(lexer.tokenize(data))
        ast.printTree()

    print("##### [TEST 2] #####")
    with open("examples/z3/ex2.txt") as file:
        data = file.read()
        ast = parser.parse(lexer.tokenize(data))
        # ast.printTree()
        
    print("##### [TEST 3] #####")
    with open("examples/z3/ex3.txt") as file:
        data = file.read()
        ast = parser.parse(lexer.tokenize(data))
        print(ast)
