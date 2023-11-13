class Node(object):
    pass

class StatementsNode(Node):
    def __init__(self, statements):
        self.statements = statements

class StatementNode(Node):
    def __init__(self, statement):
        self.statement = statement

class BreakStatement(Node):
    pass

class ContinueStatement(Node):
    pass

class ReturnStatement(Node):
    def __init__(self, expr):
        self.expr = expr

class BlankStatement(Node):
    pass

class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value

class IDNode(Node):
    def __init__(self, name):
        self.name = name

class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForNode:
    def __init__(self, variable, start, end, body):
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body

class IfElseNode:
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class AssignExpression(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class RelationExpression(Node):
    def __init__(self, op, left, right):
            self.op = op
            self.left = left
            self.right = right

class MatrixFuncNode(Node):
    def __init__(self, func_name, arg):
        self.func_name = func_name
        self.arg = arg

class ZerosNode(MatrixFuncNode):
    pass

class OnesNode(MatrixFuncNode):
    pass

class EyeNode(MatrixFuncNode):
    pass

class MatrixRefNode(Node):
    def __init__(self, id, values):
        self.id = id
        self.values = values

class IDRefNode(Node):
    def __init__(self, value):
        self.value = value

class PrintNode(Node):
    def __init__(self, value):
        self.value = value

class PrintRekNode(Node):
    def __init__(self, values):
        self.values = values

class StringOfNumNode(Node):
    def __init__(self, values):
        self.values = values     

class ExpressionNode(Node):
    def __init__(self, expr):
        self.expr = expr

class NegationNode(Node):
    def __init__(self, expr):
        self.expr = expr

class TransposeNode(Node):
    def __init__(self, expr):
        self.expr = expr

class MatrixNode(Node):
    def __init__(self, values):
        self.values = values

class MatrixRowsNode(Node):
    def __init__(self, values):
        self.values = values

class Error(Node):
    def __init__(self):
        pass
      