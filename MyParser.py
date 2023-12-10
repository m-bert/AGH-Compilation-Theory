from sly import Parser
from MyScanner import MyLexer
import AST
from TreePrinter import *


class MyParser(Parser):
    tokens = MyLexer.tokens
    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', IFX),
        ('nonassoc', ELSE),
        ('nonassoc', LTE, GTE, EQ, NEQ, LT, GT),
        ('left', ADD, SUB, DOTADD, DOTSUB),
        ('left', MUL, DIV, DOTMUL, DOTDIV),
        ('nonassoc', "'")
    )

    @_('statements stmt',
       'stmt')
    def statements(self, p):
        if len(p) == 1:
            return AST.StatementsNode([p[0]], lineno=p.lineno)

        statements = p[0].statements.copy()
        statements.append(p[1])

        return AST.StatementsNode(statements, lineno=p.lineno)

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
        try:
            if (p.BREAK):
                return AST.BreakStatement(lineno=p.lineno)
        except:
            pass
        try:
            if (p.CONTINUE):
                return AST.ContinueStatement(lineno=p.lineno)
        except:
            pass
        try:
            if (p.RETURN):
                return AST.ReturnStatement(p[1], lineno=p.lineno)
        except:
            pass

        if p[0] == ";":
            return AST.BlankStatement(lineno=p.lineno)

        if len(p) == 1:
            return p[0]

        return p[1]

    @_('IF "(" relation_expr ")" stmt ELSE stmt',
       'IF "(" relation_expr ")" stmt %prec IFX')
    def if_stmt(self, p):
        condition = p[2]
        if_body = p[4]
        else_body = None

        try:
            if (p.ELSE):
                else_body = p[6]
        except:
            pass

        return AST.IfElseNode(condition, if_body, else_body, lineno=p.lineno)

    @_('WHILE "(" relation_expr ")" stmt')
    def while_stmt(self, p):
        condition = p.relation_expr
        body = p.stmt

        return AST.WhileNode(condition, body, lineno=p.lineno)

    @_('FOR ID "=" id_int ":" id_int stmt')
    def for_stmt(self, p):
        variable = p.ID
        start = p.id_int0
        end = p.id_int1
        body = p.stmt

        return AST.ForNode(variable, start, end, body, lineno=p.lineno)

    @_('ID',
       'INTNUM')
    def id_int(self, p):
        try:
            if (p.INTNUM):
                return AST.IntNum(p[0], lineno=p.lineno)
        except:
            pass
        try:
            if (p.ID):
                return AST.IDNode(p[0], lineno=p.lineno)
        except:
            pass

    @_('PRINT print_rek ";"')
    def print_stmt(self, p):
        return AST.PrintNode(p[1],lineno=p.lineno)

    @_('print_rek "," expr',
       'expr')
    def print_rek(self, p):
        if len(p) == 3:
            values = p.print_rek.values + [p.expr]
        else:
            values = [p.expr]

        return AST.PrintRekNode(values, lineno=p.lineno)

    @_('INTNUM',
       'FLOAT',
       'ID',
       'STRING')
    def value(self, p):
        try:
            if (p.INTNUM or p.INTNUM == 0):
                return AST.IntNum(p[0], lineno=p.lineno)
        except:
            pass
        try:
            if (p.FLOAT or p.FLOAT == 0.0):
                return AST.FloatNum(p[0], lineno=p.lineno)
        except:
            pass
        try:
            if (p.ID):
                return AST.IDNode(p[0], lineno=p.lineno)
        except:
            pass
        try:
            if (p.STRING):
                return AST.Variable(p[0], lineno=p.lineno)
        except:
            pass

        return None

    @_('value',
       'assign_expr',
       'relation_expr',
       'matrix_funcs',
       'matrix_ref',
       'SUB expr',
       '"[" matrix_rows "]"',
       '"[" string_of_num "]"',
       'expr "\'"')
    def expr(self, p):
        if len(p) == 1:
            return AST.ExpressionNode(p[0], lineno=p.lineno)

        try:
            if (p.SUB):
                return AST.NegationNode(p[1], lineno=p.lineno)
        except:
            pass

        if p[1] == "'":
            return AST.TransposeNode(p[0], lineno=p.lineno)

        return AST.MatrixNode(p[1], lineno=p.lineno)

    @_('expr ADD expr',
       'expr SUB expr',
       'expr MUL expr',
       'expr DIV expr')
    def expr(self, p):
        return AST.BinExpr(p[1], p[0], p[2], lineno=p.lineno)

    @_('expr DOTADD expr',
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        return AST.BinExpr(p[1], p[0], p[2], lineno=p.lineno)

    @_('id_ref "=" expr ";"',
       'id_ref ADDASSIGN expr ";"',
       'id_ref SUBASSIGN expr ";"',
       'id_ref MULASSIGN expr ";"',
       'id_ref DIVASSIGN expr ";"',)
    def assign_expr(self, p):
        return AST.AssignExpression(p[0], p[1], p[2], lineno=p.lineno)

    @_('ID',
       'matrix_ref')
    def id_ref(self, p):
        try:
            if (p.matrix_ref):
                return p[0]
        except:
            pass

        return AST.IDRefNode(p[0], lineno=p.lineno)

    @_('expr LT expr',
       'expr GT expr',
       'expr LTE expr',
       'expr GTE expr',
       'expr EQ expr',
       'expr NEQ expr',)
    def relation_expr(self, p):
        return AST.RelationExpression(p[1], p[0], p[2], lineno=p.lineno)

    @_('ZEROS "(" INTNUM ")"',
       'ONES "(" INTNUM ")"',
       'EYE "(" INTNUM ")"')
    def matrix_funcs(self, p):
        func_name = p[0]
        arg = p[2]

        if func_name == 'zeros':
            return AST.ZerosNode(func_name, arg, lineno=p.lineno)
        elif func_name == 'ones':
            return AST.OnesNode(func_name, arg, lineno=p.lineno)
        elif func_name == 'eye':
            return AST.EyeNode(func_name, arg, lineno=p.lineno)

    @_('ID "[" string_of_num "]"')
    def matrix_ref(self, p):
        return AST.MatrixRefNode(p[0], p[2], lineno=p.lineno)

    @_('"[" string_of_num "]"',
       'matrix_rows "," "[" string_of_num "]"')
    def matrix_rows(self, p):
        if len(p) == 3:
            return AST.MatrixRowsNode([p[1]], lineno=p.lineno)

        rows = p[0].values.copy()
        rows.append(p[3])

        return AST.MatrixRowsNode(rows, lineno=p.lineno)

    @_('INTNUM',
       'string_of_num "," INTNUM')
    def string_of_num(self, p):
        if len(p) == 1:
            values = [p[0]]
        else:
            values = p[0].values.copy()
            values.append(p[2])

        return AST.StringOfNumNode(values, lineno=p.lineno)


if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    tp = TreePrinter()

    print("##### [TEST 1] #####")
    with open("examples/z2/ex1.txt") as file:
        data = file.read()
        ast = parser.parse(lexer.tokenize(data))
        # ast.printTree()

    print("##### [TEST 2] #####")
    with open("examples/z2/ex2.txt") as file:
        data = file.read()
        ast = parser.parse(lexer.tokenize(data))
        ast.printTree()

    print("##### [TEST 3] #####")
    with open("examples/z2/ex3.txt") as file:
        data = file.read()
        ast = parser.parse(lexer.tokenize(data))
