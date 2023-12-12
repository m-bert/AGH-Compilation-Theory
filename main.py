from MyParser import MyParser
from MyScanner import MyLexer
from TypeChecker import TypeChecker
from Interpreter import Interpreter

EXAMPLES = ["fibonacci", "pi", "triangle", "sqrt", "primes", "matrix"]


if __name__ == '__main__':
    for example in EXAMPLES:
        with open(f"./examples/z5/{example}.m", "r") as f:
            print(f"===============================")
            print(f"RUNNING {example}")
            print(f"===============================")
            data = f.read()
            
            lexer = MyLexer()
            parser = MyParser()
            typeChecker = TypeChecker()
            interpreter = Interpreter()

            ast = parser.parse(lexer.tokenize(data))

            try:
                typeChecker.visit(ast)
            except:
                print("- TYPE CHECKER ERROR -")
                typeChecker.print_errors()
            else:
                interpreter.visit(ast)
                
            print()
