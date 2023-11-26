import AST
from SymbolTable import SymbolTable, VariableSymbol


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for _, value in node.__dict__.items():
            if isinstance(value, list):  # xd
                for item in value:
                    if isinstance(item, AST.Node):
                        self.visit(item)
            elif isinstance(value, AST.Node):
                self.visit(value)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.errors = []
        self.symbol_table = SymbolTable(None, "program")
        self.current_scope = self.symbol_table

    def new_error(self, line, message):
        self.errors.append(f"Error at line {line}: {message}")

    def visit_StatementsNode(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_AssignExpression(self, node):
        # ADD NEW VAR TO SCOPE
        var_name = node.left.value
        var_type = "var"
        size = None
        # z jakiegoś powodu MatrixNode nie jest z ExpressionNode a reszta tak
        if (isinstance(node.right, AST.MatrixNode)):
            var_type = "mat"
            size = len(node.right.values.values)
        elif (isinstance(node.right.expr, AST.IntNum)):
            var_type = "int"
        elif (isinstance(node.right.expr, AST.FloatNum)):
            var_type = "float"
        elif (isinstance(node.right.expr, AST.Variable)):
            # to mogłoby się nazywać string zamiast variable
            var_type = "string"
        elif (isinstance(node.right.expr, AST.ZerosNode) or
              isinstance(node.right.expr, AST.OnesNode) or
              isinstance(node.right.expr, AST.EyeNode)):
            var_type = "mat"
            size = node.right.expr.arg

        var = VariableSymbol(var_name, var_type, size)
        self.current_scope.put(var_name, var)
        # ----------------------

        self.visit(node.left)
        self.visit(node.right)

        # MATRIX INITIALIZATION CHECK
        if (isinstance(node.right, AST.MatrixNode)):
            row_len = -1
            if (isinstance(node.right.values, AST.MatrixRowsNode)):
                for row in node.right.values.values:  # xd2
                    if (row_len == -1):
                        row_len = len(row.values)
                    elif (len(row.values) != row_len):
                        self.new_error(0, "Incorrect size of matrix rows!")
                        return
        # -----------------------------

    def visit_RelationExpression(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_IDRefNode(self, node):
        pass

    def visit_ExpressionNode(self, node):
        self.visit(node.expr)

    def visit_ZerosNode(self, node):
        # u nas w sumie parser to robi. Nie wiem czy to dobrze
        pass

    def visit_OnesNode(self, node):
        pass

    def visit_EyeNode(self, node):
        pass

    def visit_MatrixNode(self, node):
        self.visit(node.values)

    def visit_MatrixRowsNode(self, node):
        for value in node.values:
            self.visit(value)

    def visit_StringOfNumNode(self, node):
        pass

    def visit_MatrixRefNode(self, node):
        self.visit(node.values)

        # MATRIX BOUNDS CHCECK
        matrix = self.symbol_table.get(node.id)
        if (not matrix):
            self.new_error(0, "Unknown variable!")
            return
        if (matrix.size == None):
            self.new_error(0, "wtf")

        args = node.values.values
        if (len(args) == 1):
            if (args[0] >= matrix.size):
                self.new_error(0, "Out of array scope!")
        elif (len(args) == 2):
            print("asdf")

        # kurde faja, więcej wymiarów może być
        # może założymy że maks dwuwymiarowe xD

    def visit_IntNum(self, node):
        pass
        pass

    def visit_FloatNum(self, node):
        pass

    def visit_NegationNode(self, node):
        self.visit(node.expr)

    def visit_IDNode(self, node):
        pass

    def visit_TransposeNode(self, node):
        self.visit(node.expr)

    def visit_BinExpr(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_ForNode(self, node):
        self.current_scope = SymbolTable(self.current_scope, "for")

        self.visit(node.start)
        self.visit(node.end)
        self.visit(node.body)

        self.current_scope = self.current_scope.parent

    def visit_PrintNode(self, node):
        self.visit(node.value)

    def visit_PrintRekNode(self, node):
        for value in node.values:
            self.visit(value)

    def visit_WhileNode(self, node):
        self.current_scope = SymbolTable(self.current_scope, "while")

        self.visit(node.condition)
        self.visit(node.body)

        self.current_scope = self.current_scope.parent

    def visit_IfElseNode(self, node):
        self.current_scope = SymbolTable(self.current_scope, "if")

        self.visit(node.condition)
        self.visit(node.if_body)

        self.current_scope = self.current_scope.parent
        if (node.else_body == None):
            return

        self.current_scope = SymbolTable(self.current_scope, "else")

        self.visit(node.else_body)

        self.current_scope = self.current_scope.parent

    def visit_BreakStatement(self, node):
        # IN LOOP CHECK
        if (not (self.current_scope.name == "for" or
           self.current_scope.name == "while")):
            self.new_error(0, "Incorrect break statement use!")

    def visit_ContinueStatement(self, node):
        if (not (self.current_scope.name == "for" or
           self.current_scope.name == "while")):
            self.new_error(0, "Incorrect continue statement use!")

    def visit_ReturnStatement(self, node):
        pass

    # ------------------------------------

    def print_errors(self):
        for error in self.errors:
            print(error)

    def print_symbols(self, scope):
        if (scope.parent != None):
            self.print_symbols(self, scope.parent)
        for name, symbol in scope.symbols.items():
            if (symbol.type == "mat"):
                print(
                    f"{scope.name.upper()} -> name: {name}, type: {symbol.type}, size: {symbol.size}")
            else:
                print(f"{scope.name.upper()} -> name: {name}, type: {symbol.type}")
