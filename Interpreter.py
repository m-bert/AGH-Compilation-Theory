
import AST
from Memory import *
from Exceptions import  *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

class Interpreter(object):

    def __init__(self):
        self.ops = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,

            ".+": lambda A, B: A + B,
            ".-": lambda A, B: A - B,
            ".*": lambda A, B: A @ B,
            "./": lambda A, B: A @ np.linalg.inv(B),

            "+=": lambda a, b: a + b,
            "-=": lambda a, b: a - b,
            "*=": lambda a, b: a * b,
            "/=": lambda a, b: a / b,

            "<": lambda a, b: a < b,
            "<=": lambda a, b: a <= b,
            ">": lambda a, b: a > b,
            ">=": lambda a, b: a >= b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b
        }

        self.global_memory = Memory("global")
        self.memory_stack = MemoryStack(self.global_memory)

    def add_scope(self, name = ""):
        memory = Memory(name)
        self.memory_stack.push(memory)

        return
    
    def pop_scope(self):
        self.memory_stack.pop()

        return

    @on('node')
    def visit(self, node):
        pass

    @when(AST.StatementsNode)
    def visit(self, node):
        for statement in node.statements:
            self.visit(statement)
        return

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)

        return self.ops[node.op](r1, r2)

    @when(AST.AssignExpression)
    def visit(self, node):
        var_name = self.visit(node.left)
        update_value = self.visit(node.right)

        var_value = update_value

        if(isinstance(node.left, AST.MatrixRefNode)):
            matrix, indexes = var_name
            matrix[indexes[0], indexes[1]] = var_value

            self.memory_stack.set(node.left.id, matrix)

            return

        if node.operator != '=':
            current_var_value = self.memory_stack.get(var_name)
            var_value = self.ops[node.operator](current_var_value, update_value)
           
        self.memory_stack.set(var_name, var_value)
        

    @when(AST.ExpressionNode)
    def visit(self, node):
        return self.visit(node.expr)
    
    @when(AST.EyeNode)
    def visit(self, node):
        matrix = [[1 if i == j else 0 for j in range(node.arg)]
                  for i in range(node.arg)]
        
        return np.array(matrix)
    
    @when(AST.OnesNode)
    def visit(self, node):
        matrix = [[1 for _ in range(node.arg)]
                  for _ in range(node.arg)]
        
        return np.array(matrix)
    
    @when(AST.ZerosNode)
    def visit(self, node):
        matrix = [[0 for _ in range(node.arg)]
                  for _ in range(node.arg)]
        
        return np.array(matrix)

    
    @when(AST.IntNum)
    def visit(self, node):
        return node.value
    
    @when(AST.FloatNum)
    def visit(self, node):
        return node.value
    
    @when(AST.Variable)
    def visit(self, node):
        return node.name
    
    @when(AST.IDNode)
    def visit(self, node):
        return self.memory_stack.get(node.name)
    
    @when(AST.IDRefNode)
    def visit(self, node):
        return node.value
    
    @when(AST.MatrixRefNode)
    def visit(self, node):
        matrix = self.memory_stack.get(node.id)
        indexes = self.visit(node.values)

        return matrix, indexes
    
    @when(AST.StringOfNumNode)
    def visit(self, node):
        return node.values
    
    @when(AST.PrintNode)
    def visit(self, node):
        self.visit(node.value)

    @when(AST.PrintRekNode)
    def visit(self, node):
        for value in node.values:
            res = self.visit(value)
            
            if isinstance(res, tuple):
                print(res[0][res[1][0], res[1][1]])
            else:
                print(res)

    @when(AST.RelationExpression)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)

        return self.ops[node.op](r1, r2)
    
    @when(AST.BreakStatement)
    def visit(self, node):
        raise BreakException()
    
    @when(AST.ContinueStatement)
    def visit(self, node):
        raise ContinueException()
    
    @when(AST.ReturnStatement)
    def visit(self, node):
        print(self.visit(node.expr))
        sys.exit(0)
    
    @when(AST.IfElseNode)
    def visit(self, node):
        if self.visit(node.condition):
            self.visit(node.if_body)
        else:
            self.visit(node.else_body)

    @when(AST.WhileNode)
    def visit(self, node):
        self.add_scope("while")

        while self.visit(node.condition):
            try:
                self.visit(node.body)
            except BreakException:
                break
            except ContinueException:
                continue

    
        self.pop_scope()

    @when(AST.ForNode)
    def visit(self, node):
        self.add_scope("for")

        start = self.visit(node.start)
        end = self.visit(node.end)

        for i in range(start, end):
            self.memory_stack.set(node.variable, i)

            try:
                self.visit(node.body)
            except BreakException:
                break
            except ContinueException:
                continue
            
    
        self.pop_scope()

