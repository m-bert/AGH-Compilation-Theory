
import AST
import SymbolTable
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
            "/=": lambda a, b: a / b
        }

        self.global_memory = Memory("global")
        self.memory_stack = MemoryStack(self.global_memory)

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
        var_name = node.left.value
        update_value = self.visit(node.right)

        var_value = update_value

        if node.operator != '=':
            current_var_value = self.memory_stack.get(var_name)
            var_value = self.ops[node.operator](current_var_value, update_value)
           
        self.memory_stack.set(var_name, var_value)
        

    @when(AST.ExpressionNode)
    def visit(self, node):
        return self.visit(node.expr)
    
    @when(AST.IntNum)
    def visit(self, node):
        return node.value
    
    @when(AST.IDNode)
    def visit(self, node):
        return self.memory_stack.get(node.name)
    
    @when(AST.PrintNode)
    def visit(self, node):
        self.visit(node.value)

    @when(AST.PrintRekNode)
    def visit(self, node):
        for value in node.values:
            print(self.visit(value))



    # # simplistic while loop interpretation
    # @when(AST.WhileInstr)
    # def visit(self, node):
    #     r = None
    #     while node.cond.accept(self):
    #         r = node.body.accept(self)
    #     return r

