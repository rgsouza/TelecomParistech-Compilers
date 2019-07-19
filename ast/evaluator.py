#
# File provided by Compilers course from TelecomParitech
# Code implemented by Rayanne Souza
# Last modification: 23 Oct 2015
#

from ast.nodes import *
from utils.visitor import visitor

class Evaluator:
    """This contains a simple evaluator visitor which computes the value
    of a tiger expression."""

    @visitor(IntegerLiteral)
    def visit(self, int):
        return int.intValue

    @visitor(IfThenElse)
    def visit(self, ifCond):
        condition = ifCond.condition.accept(self)
        if (condition):
            return ifCond.then_part.accept(self)
        else:
            return ifCond.else_part.accept(self)
        
    @visitor(SeqExp)
    def visit(self, seq):

        n = len(seq.exps)
        if n:   
            for i in range(n - 1):
                seq.exps[i].accept(self)

            return seq.exps[n - 1].accept(self)

        
    @visitor(BinaryOperator)
    def visit(self, binop):
        op = binop.op

        if op == r'&' and binop.left.accept(self) == 0:
            return 0

        if op == r'|' and binop.left.accept(self) == 1:
            return 1


        left, right = binop.left.accept(self),binop.right.accept(self)
        
        if op == '+':
            return left + right

        elif op == '*':
            return left * right

        elif op == '-':
            return left - right

        elif op == '/':
            return (int)(left/right)

        elif op == '>':
            if left > right:
                return 1
            else:
                return 0

        elif op == '<':
            if left < right:
                return 1
            else:
                return 0

        elif op == '<=':
            if left <= right:
                return 1
            else:
                return 0

        elif op == '>=':
            if left >= right:
                return 1
            else:
                return 0

        elif op == '=':
            if left == right:
                return 1
            else:
                return 0

        elif op == '<>':
            if left != right:
                return 1
            else:
                return 0

        elif op == '&':
            if left and right:
                return 1
            else:
                return 0

        elif op == '|':
            if left or right:
                return 1
            else:
                return 0
    
            
        else:
            raise SyntaxError("unknown operator %s" % op)
    
    @visitor(None)
    def visit(self, node):
        raise SyntaxError("no evaluation defined for %s" % node)
