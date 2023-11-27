from MyScanner import MyLexer
from MyParser import MyParser
from TypeChecker import TypeChecker

if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    # data = """x = [ [1,2,3],
    #   [1,2,3,4,5],
    #   [1,2]
    # ];

    # print -3;

    # z = "elo" + 4;
    
    # break;
    # y = zeros(0);
    
    # """
    data = """
x = 0;
y = zeros(5);
z = x + y;

x = eye(5);
y = eye(8);
z = x + y;

x = [ 1,2,3,4,5 ];
y = [ [1,2,3,4,5],
      [1,2,3,4,5] ];
z = x + y;

x = zeros(5);
y = zeros(5);
z = x.*y;

x = ones(5);
z = x[7,10];
v = x[2,3,4];
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
