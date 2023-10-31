from sly import Lexer


class MyLexer(Lexer):
    def __init__(self):
        self.nesting_level = 0

    tokens = {
        ID,
        IF,
        ELSE,
        WHILE,
        FOR,
        BREAK,
        CONTINUE,
        RETURN,
        EYE,
        ZEROS,
        ONES,
        PRINT,
        INTNUM,
        FLOAT,

        MULASSIGN,
        SUBASSIGN,
        ADDASSIGN,
        DIVASSIGN,

        DOTADD,
        DOTSUB,
        DOTMUL,
        DOTDIV,

        ADD,
        SUB,
        MUL,
        DIV,

        LT,
        GT,
        LTE,
        GTE,
        EQ,
        NEQ,

        STRING
    }

    ignore = " \t"
    ignore_comment = "#.*"

    LTE = r"<="
    GTE = r">="
    LT = r"<"
    GT = r">"
    EQ = r"=="
    NEQ = r"!="

    MULASSIGN = r"\*="
    SUBASSIGN = r"-="
    ADDASSIGN = r"\+="
    DIVASSIGN = r"/="

    DOTADD = r"\.\+"
    DOTSUB = r"\.-"
    DOTMUL = r"\.\*"
    DOTDIV = r"\./"

    ADD = r"\+"
    SUB = r"-"
    MUL = r"\*"
    DIV = r"/"

    literals = {'(', ')', '{', '}', '[', ']', ',', ';', ':', '\'', '='}

    STRING = r"\".*\""

    ID = r"[a-zA-Z_][\w_]*"
    ID["if"] = IF
    ID["else"] = ELSE
    ID["while"] = WHILE
    ID["for"] = FOR
    ID["break"] = BREAK
    ID["continue"] = CONTINUE
    ID["return"] = RETURN
    ID["eye"] = EYE
    ID["zeros"] = ZEROS
    ID["ones"] = ONES
    ID["print"] = PRINT

    @_(r'[\{\[\(]')
    def lbrace(self, t):
        t.type = t.value
        self.nesting_level += 1
        return t

    @_(r'[\}\]\)]')
    def rbrace(self, t):
        t.type = t.value
        self.nesting_level -= 1
        return t

    @_(r"[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?")
    def FLOAT(self, t):
        t.value = float(t.value)  # Convert to a numeric value
        return t

    @_(r"\d+")
    def INTNUM(self, t):
        t.value = int(t.value)  # Convert to a numeric value
        return t

    # Define a rule so we can track line numbers
    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

    @_(r'[\d\.\?]+[a-zA-Z]*')
    def bad_token(self, t):
        print(f"ERROR: Unknown token at line {self.lineno}: {t.value}")


if __name__ == "__main__":
    data = """A = zeros(5);  # create 5x5 matrix filled with zeros
                B = ones(7);   # create 7x7 matrix filled with ones
                I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere
                D1 = A.+B' ; # add element-wise A with transpose of B
                D2 -= A.-B' ; # substract element-wise A with transpose of B
                D3 *= A.*B' ; # multiply element-wise A with transpose of B
                D4 /= A./B' ; # divide element-wise A with transpose of B

                E1 = [ [ 1, 2, 3],
                    [ 4, 5, 6],
                    [ 7, 8, 9] ];

                res1 = 60.500;
                res2 = 60.;
                res3 = .500;
                res4 = 60.52E2;
                str = "Hello world";

                a3 = ?b

                if (m==n) { 
                    if (m >= n) 
                        print res;
                }"""

    lexer = MyLexer()
    tokens = lexer.tokenize(data)

    for tok in tokens:
        print(f"({tok.lineno}): {tok.type}({tok.value})")

    if (lexer.nesting_level != 0):
        print("Error: braces are not nested correctly")

