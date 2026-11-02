"""Small exact integer expression evaluator for authored source validation."""
import ast
import math

def evaluate(expression):
    def visit(node):
        if isinstance(node,ast.Constant) and type(node.value) is int:return node.value
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):return -visit(node.operand)
        if isinstance(node,ast.BinOp):
            a,b=visit(node.left),visit(node.right)
            if isinstance(node.op,ast.Add):return a+b
            if isinstance(node.op,ast.Sub):return a-b
            if isinstance(node.op,ast.Mult):return a*b
            if isinstance(node.op,ast.FloorDiv) and b and a%b==0:return a//b
            if isinstance(node.op,ast.Pow) and 0<=b<=4:return a**b
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and len(node.args)==1 and not node.keywords:
            a=visit(node.args[0]);name=node.func.id
            if name=='sqrt' and a>=0:
                v=math.isqrt(a)
                if v*v==a:return v
            if name=='cbrt':
                v=math.isqrt(abs(a))
                v=next((x for x in range(v+1) if x*x*x==abs(a)),None)
                if v is not None:return v if a>=0 else -v
        raise ValueError(f'Unsupported or non-integral expression: {expression}')
    return visit(ast.parse(expression,mode='eval').body)
