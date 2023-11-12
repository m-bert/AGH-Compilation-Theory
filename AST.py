class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):

    def __init__(self, value):
        self.value = value

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

class AssignExprNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class AssignNode(AssignExprNode):
    pass

class AddAssignNode(AssignExprNode):
    pass

class SubAssignNode(AssignExprNode):
    pass

class MulAssignNode(AssignExprNode):
    pass

class DivAssignNode(AssignExprNode):
    pass


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

class Error(Node):
    def __init__(self):
        pass
      