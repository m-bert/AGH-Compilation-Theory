from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.StatementsNode)
    def printTree(self, indent=0):
        for stmt in self.statements:
            stmt.printTree(indent)

    @addToClass(AST.AssignExpression)
    def printTree(self, indent=0):
        print(self.operator)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.IDRefNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.value}")

    @addToClass(AST.ExpressionNode)
    def printTree(self, indent=0):
        self.expr.printTree(indent)

    @addToClass(AST.ZerosNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}ZEROS")
        print(f"{'|  ' * (indent + 1)}{self.arg}")

    @addToClass(AST.OnesNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}ONES")
        print(f"{'|  ' * (indent + 1)}{self.arg}")

    @addToClass(AST.EyeNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}EYE")
        print(f"{'|  ' * (indent + 1)}{self.arg}")

    @addToClass(AST.MatrixNode)
    def printTree(self, indent=0):
        self.values.printTree(indent)

    @addToClass(AST.MatrixRowsNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}VECTOR")
        for value in self.values:
            value.printTree(indent + 1)

    @addToClass(AST.StringOfNumNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}VECTOR")
        for value in self.values:
            print(f"{'|  ' * (indent + 1)}{value}")

    @addToClass(AST.MatrixRefNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}REF")
        print(f"{'|  ' * (indent + 1)}{self.id}")
        self.values.printTree(indent)
        
    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.value}")
        
    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.value}")
        
    @addToClass(AST.NegationNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}-")
        self.expr.printTree(indent)
        
    @addToClass(AST.IDNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.name}")

    @addToClass(AST.TransposeNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}TRANSPOSE")
        self.expr.printTree(indent + 1)


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass    
        # fill in the body


    # define printTree for other classes
    # ...

