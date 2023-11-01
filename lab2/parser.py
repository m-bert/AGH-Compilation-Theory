from sly import Parser
from scaner import MyLexer

class MyParser(Parser):
    tokens = MyLexer.tokens
    debugfile = 'parser.out'
    
    precedence = (
        ('nonassoc', IFX),
        ('nonassoc', ELSE),
        ('nonassoc', LTE, GTE, EQ, NEQ, LT, GT),
        ('left', ADD, SUB),
        ('left', MUL, DIV),
        ('left', DOTADD, DOTSUB),
        ('left', DOTMUL, DOTDIV)
    )
    
    @_('statements stmt',
       'stmt')
    def statements(self, p):
        return None
    
    @_('";"',
       '"{" statements "}"',
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
    
    @_('IF "(" relation_expr ")" stmt ELSE stmt',
       'IF "(" relation_expr ")" stmt %prec IFX')
    def if_stmt(self, p):
        return None
    
    @_('WHILE "(" relation_expr ")" stmt')
    def while_stmt(self, p):
        return None
    
    @_('FOR ID "=" id_int ":" id_int stmt')
    def for_stmt(self, p):
        return None
    
    @_('ID',
       'INTNUM')
    def id_int(self, p):
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
    
    @_('value',
       'assign_expr',
       'relation_expr',
       'matrix_funcs',
       'matrix_ref',
       'SUB expr',
       '"[" matrix_rows "]"',
       'expr "\'"')
    def expr(self, p):
        return None
    
    @_('expr ADD expr',
       'expr SUB expr',
       'expr MUL expr',
       'expr DIV expr')
    def expr(self, p):
        return None
    
    @_('expr DOTADD expr',
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        return None
    
    @_('id_ref "=" expr ";"',
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
    
    @_('ZEROS "(" INTNUM ")"',
       'ONES "(" INTNUM ")"',
       'EYE "(" INTNUM ")"')
    def matrix_funcs(self, p):
        return None
    
    @_('ID "[" string_of_num "]"')
    def matrix_ref(self, p):
        return None
    
    @_('"[" string_of_num "]"',
      'matrix_rows "," "[" string_of_num "]"')
    def matrix_rows(self, p):
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
    
    