from sly import Parser
from scaner import MyLexer

# nie wiem czy akceptujemy na przykład x += "cos", "costam" < "cos2" itd. (pewnie do zmiany)
# czy możena np. return k += 5

class MyParser(Parser):
    tokens = MyLexer.tokens
    
    precedence = (
        ('left', ADD, SUB),
        ('left', MUL, DIV),
        ('left', DOTADD, DOTSUB),
        ('left', DOTMUL, DOTDIV),
        ('nonassoc', LTE, GTE, EQ, NEQ, LT, GT)
    )
    
    @_('statements stmt_braces',
       'stmt_braces')
    def statements(self, p):
        return None
    
    @_('";"',
       'if_stmt',
       'while_stmt',
       'for_stmt',
       'assign_expr',
       'print_stmt',
       'BREAK ";"',
       'CONTINUE ";"',
       'RETURN expr ";"')
    def stmt(self, p):
        return None
    
    @_('IF "(" bool_expr ")" stmt_braces',
       'IF "(" bool_expr ")" stmt_braces ELSE stmt_braces')
    def if_stmt(self, p):
        return None
    
    @_('WHILE "(" bool_expr ")" stmt_braces')
    def while_stmt(self, p):
        return None
    
    @_('FOR ID "=" id_int ":" id_int stmt_braces')
    def for_stmt(self, p):
        return None
    
    @_('ID',
       'INTNUM')
    def id_int(self, p):
        return None
    
    @_('"{" statements "}"',
       'stmt')
    def stmt_braces(self, p):
        return None
    
    @_('PRINT print_rek ";"')
    def print_stmt(self, p):
        return None
    
    @_('print_rek "," value',
       'value')
    def print_rek(self, p):
        return None
    
    @_('INTNUM',
       'FLOAT',
       'ID',
       'STRING')
    def value(self, p):
        return None
    
    @_('SUB ID',
       'SUB INTNUM',
       'SUB FLOAT')
    def inv_num(self, p):
        return None
    
    @_('value',
       'inv_num',
       'bin_expr',
       'assign_expr',
       'relation_expr',
       'matrix_bin_expr',
       'matrix_transpose',
       'matrix_funcs',
       'matrix_ref')
    def expr(self, p):
        return None
    
    @_('bin_expr',
       'relation_expr')
    def bool_expr(self, p):
        return None
    
    @_('expr ADD expr',
       'expr SUB expr',
       'expr MUL expr',
       'expr DIV expr')
    def bin_expr(self, p):
        return None
    
    @_('id_ref "=" expr ";"',
       'id_ref "=" matrix ";"',
       'id_ref ADDASSIGN expr ";"',
       'id_ref SUBASSIGN expr ";"',
       'id_ref MULASSIGN expr ";"',
       'id_ref DIVASSIGN expr ";"',)
    def assign_expr(self, p):
        return None
    
    @_('ID',
       'matrix_ref')
    def id_ref(self, p):
        return None
    
    @_('expr LT expr',
       'expr GT expr',
       'expr LTE expr',
       'expr GTE expr',
       'expr EQ expr',
       'expr NEQ expr',)
    def relation_expr(self, p):
        return None
    
    @_('expr DOTADD expr',
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def matrix_bin_expr(self, p):
        return None
    
    @_('ID "\'"',
       'matrix "\'"')
    def matrix_transpose(self, p):
        return None
    
    @_('ZEROS "(" INTNUM ")"',
       'ONES "(" INTNUM ")"',
       'EYE "(" INTNUM ")"')
    def matrix_funcs(self, p):
        return None
    
    @_('ID "[" string_of_num "]"')
    def matrix_ref(self, p):
        return None
    
    @_('"[" "]"',
       '"[" matrix_rows "]"')
    def matrix(self, p):
        return None
    
    @_('matrix_row',
      'matrix_rows "," matrix_row')
    def matrix_rows(self, p):
        return None
    
    @_('"[" "]"',
       '"[" string_of_num "]"')
    def matrix_row(self, p):
        return None
    
    @_('INTNUM',
       'string_of_num "," INTNUM')
    def string_of_num(self, p):
        return None
    

if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    print("##### [TEST 1] #####")
    with open("lab2\ex1.txt") as file:
        data = file.read()
        parser.parse(lexer.tokenize(data))
        
    print("##### [TEST 2] #####")
    with open("lab2\ex2.txt") as file:
        data = file.read()
        parser.parse(lexer.tokenize(data))
        
    print("##### [TEST 3] #####")
    with open("lab2\ex3.txt") as file:
        data = file.read()
        parser.parse(lexer.tokenize(data))
    
    