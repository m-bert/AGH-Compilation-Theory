from sly import Parser
from MyScanner import MyLexer
import AST

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
        condition = p.relation_expr
        if_body = p.stmt0
        else_body = p.stmt1 if len(p) > 4 else None

        return AST.IfElseNode(condition, if_body, else_body)

    @_('WHILE "(" relation_expr ")" stmt')
    def while_stmt(self, p):
        condition = p.relation_expr
        body = p.stmt

        return AST.WhileNode(condition, body)
    
    @_('FOR ID "=" id_int ":" id_int stmt')
    def for_stmt(self, p):
        variable = p.ID
        start = p.id_int0
        end = p.id_int1
        body = p.stmt

        return AST.ForNode(variable, start, end, body)
    
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
        return AST.BinExpr(p[1], p[0], p[2])
    
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
        left = p.id_ref
        operator = p[1]  # Assuming the operator type is accessible like this
        right = p.expr

        if operator == '=':
            return AST.AssignNode(left, operator, right)
        elif operator == '+=':
            return AST.AddAssignNode(left, operator, right)
        elif operator == '-=':
            return AST.SubAssignNode(left, operator, right)
        elif operator == '*=':
            return AST.MulAssignNode(left, operator, right)
        elif operator == '/=':
            return AST.DivAssignNode(left, operator, right)
        
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
        return AST.RelationExpression(p[1], p[0], p[2])
    
    @_('ZEROS "(" INTNUM ")"',
       'ONES "(" INTNUM ")"',
       'EYE "(" INTNUM ")"')
    def matrix_funcs(self, p):
        func_name = p[0]
        arg = p[2]
        
        if func_name == 'zeros':
            return AST.ZerosNode(func_name, arg)
        elif func_name == 'ones':
            return AST.OnesNode(func_name, arg)
        elif func_name == 'eye':
            return AST.EyeNode(func_name, arg)
    
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
    with open("examples/z2/ex1.txt") as file:
        data = file.read()
        ast = parser.parse(lexer.tokenize(data))
        print(ast)
    # print("##### [TEST 2] #####")
    # with open("examples/z2/ex2.txt") as file:
    #     data = file.read()
    #     parser.parse(lexer.tokenize(data))
        
    # print("##### [TEST 3] #####")
    # with open("examples/z2/ex3.txt") as file:
    #     data = file.read()
    #     parser.parse(lexer.tokenize(data))
    
    