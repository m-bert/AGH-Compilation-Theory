from sly import Lexer


class MyLexer(Lexer):
    tokens = {
        ID,
        BINARY,
        MATBIN,
        ASSIGNMENT,
        RELATION,
        BRACES,
        RANGE,
        TRANSPOSE,
        COMMA,
        SEMICOLON,
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
        NUMBER,
        FLOAT,
    }

    ignore = " \t"
    ignore_comment = "#.*"

    BINARY = r"[\+\-\/\*]"
    MATBIN = r"[.][\+\-\/\*]"
    RELATION = r"[<>]=?|[!=]="
    ASSIGNMENT = r"[\+\-\*\/]?="
    BRACES = r"[()\[\]{}]"
    RANGE = r":"
    TRANSPOSE = r"\'"
    COMMA = r","
    SEMICOLON = r";"

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

    @_(r"\d+\.\d+")
    def FLOAT(self, t):
        t.value = float(t.value)  # Convert to a numeric value
        return t

    @_(r"\d+")
    def NUMBER(self, t):
        t.value = int(t.value)  # Convert to a numeric value
        return t

    # Define a rule so we can track line numbers
    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)


if __name__ == "__main__":
    data = """
        A = zeros(5); # create 5x5 matrix filled with zeros
        B = ones(7);  # create 7x7 matrix filled with ones
        I = eye(10);  # create 10x10 matrix filled with ones on diagonal and zeros elsewhere
        D1 = A.+B' ;  # add element-wise A with transpose of B
        D2 -= A.-B' ; # substract element-wise A with transpose of B
        D3 *= A.*B' ; # multiply element-wise A with transpose of B
        D4 /= A./B' ; # divide element-wise A with transpose of B
    """
    lexer = MyLexer()
    for tok in lexer.tokenize(data):
        print(f'({tok.lineno}): {tok.type}({tok.value})')
