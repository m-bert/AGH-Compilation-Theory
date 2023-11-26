from MyScanner import MyLexer
from MyParser import MyParser
from TypeChecker import TypeChecker

if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    # data = """x=0;
    #         continue;
    #         return x;
    #         break;
    #         return x+1;
    #         return 2*x;
    #         print x;"""

    data = """x = [ [1,2,3],
      [1,2,3,4,5],
      [1,2]
    ];
    
    break;
    y = zeros(5);
    
    """

    ast = parser.parse(lexer.tokenize(data))

    typeChecker = TypeChecker()

    typeChecker.visit(ast)

    print()
    print("-------- VARIABLES ----------")
    typeChecker.print_symbols(typeChecker.current_scope)

    print()
    print("-------- ERRORS ----------")
    typeChecker.print_errors()
