class Node(object):
    def __init__(self, lineno):
        self.lineno = lineno
    pass

class StatementsNode(Node):
    def __init__(self, statements, lineno):
        super().__init__(lineno)
        self.statements = statements

class StatementNode(Node):
    def __init__(self, statement, lineno):
        super().__init__(lineno)
        self.statement = statement

class BreakStatement(Node):
    def __init__(self, lineno):
        super().__init__(lineno)
    pass

class ContinueStatement(Node):
    def __init__(self, lineno):
        super().__init__(lineno)
    pass

class ReturnStatement(Node):
    def __init__(self, expr, lineno):
        super().__init__(lineno)
        self.expr = expr

class BlankStatement(Node):
    def __init__(self, lineno):
        super().__init__(lineno)
    pass

class IntNum(Node):
    def __init__(self, value, lineno):
        super().__init__(lineno)
        self.value = value

class FloatNum(Node):
    def __init__(self, value, lineno):
        super().__init__(lineno)
        self.value = value

class IDNode(Node):
    def __init__(self, name, lineno):
        super().__init__(lineno)
        self.name = name

class WhileNode(Node):
    def __init__(self, condition, body, lineno):
        super().__init__(lineno)
        self.condition = condition
        self.body = body

class ForNode(Node):
    def __init__(self, variable, start, end, body, lineno):
        super().__init__(lineno)
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body

class IfElseNode(Node):
    def __init__(self, condition, if_body, else_body=None, lineno=0):
        super().__init__(lineno)
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class AssignExpression(Node):
    def __init__(self, left, operator, right, lineno):
        super().__init__(lineno)
        self.left = left
        self.operator = operator
        self.right = right

class Variable(Node):
    def __init__(self, name, lineno):
        super().__init__(lineno)
        self.name = name.strip("\"")


class BinExpr(Node):
    def __init__(self, op, left, right, lineno):
        super().__init__(lineno)
        self.op = op
        self.left = left
        self.right = right

class RelationExpression(Node):
    def __init__(self, op, left, right, lineno):
            super().__init__(lineno)
            self.op = op
            self.left = left
            self.right = right

class MatrixFuncNode(Node):
    def __init__(self, func_name, arg, lineno):
        super().__init__(lineno)
        self.func_name = func_name
        self.arg = arg

class ZerosNode(MatrixFuncNode):
    def __init__(self, func_name, arg, lineno):
        super().__init__(func_name, arg, lineno)
    pass

class OnesNode(MatrixFuncNode):
    def __init__(self, func_name, arg, lineno):
        super().__init__(func_name, arg, lineno)
    pass

class EyeNode(MatrixFuncNode):
    def __init__(self, func_name, arg, lineno):
        super().__init__(func_name, arg, lineno)
    pass

class MatrixRefNode(Node):
    def __init__(self, id, values, lineno):
        super().__init__(lineno)
        self.id = id
        self.values = values

class IDRefNode(Node):
    def __init__(self, value, lineno):
        super().__init__(lineno)
        self.value = value

class PrintNode(Node):
    def __init__(self, value, lineno):
        super().__init__(lineno)
        self.value = value

class PrintRekNode(Node):
    def __init__(self, values, lineno):
        super().__init__(lineno)
        self.values = values

class StringOfNumNode(Node):
    def __init__(self, values, lineno):
        super().__init__(lineno)
        self.values = values     

class ExpressionNode(Node):
    def __init__(self, expr, lineno):
        super().__init__(lineno)
        self.expr = expr

class NegationNode(Node):
    def __init__(self, expr, lineno):
        super().__init__(lineno)
        self.expr = expr

class TransposeNode(Node):
    def __init__(self, expr, lineno):
        super().__init__(lineno)
        self.expr = expr

class MatrixNode(Node):
    def __init__(self, values, lineno):
        super().__init__(lineno)
        self.values = values

class MatrixRowsNode(Node):
    def __init__(self, values, lineno):
        super().__init__(lineno)
        self.values = values

class Error(Node):
    def __init__(self, lineno):
        super().__init__(lineno)
        pass
      