#
# File provided by Compilers course from TelecomParitech
# Code implemented by Rayanne Souza
# Last modification: 24 Oct 2015
#


from ast.nodes import *
from utils.visitor import *


class Dumper(Visitor):

    def __init__(self, semantics):
        """Initialize a new Dumper visitor. If semantics is True,
        additional information will be printed along with declarations
        and identifiers."""
        self.semantics = semantics

    @visitor(None)
    def visit(self, node):
        raise Exception("unable to dump %s" % node)

    @visitor(IntegerLiteral)
    def visit(self, i):
        return str(i.intValue)

    @visitor(BinaryOperator)
    def visit(self, binop):
        # Always use parentheses to reflect grouping and associativity,
        # even if they may be superfluous.
        return "(%s %s %s)" % \
               (binop.left.accept(self), binop.op, binop.right.accept(self))

    @visitor(Let)
    def visit(self, let):

        decls = ""
        expressions = ""

        #exps = let.exps[0].accept(self)
        n = len(let.decls)

        for i in range(n):
            decls = decls + let.decls[i].accept(self)
            if i != n-1:
                decls += " "

        if len(let.exps)!=0:
            n = len(let.exps)
            for i in range(n):
                expressions += let.exps[i].accept(self)

                if i!= n -1:
                    expressions += "; "
                
        return "let %s in %s end" % (decls,  expressions)

    @visitor(VarDecl)
    def visit(self, decl):
        
        if decl.type and decl.exp is not None :

            if decl.type.accept(self)!="void":
                if decl.escapes and self.semantics:
                    return "var %s/*e*/: %s := %s" %(decl.name, decl.type.accept(self), decl.exp.accept(self))
                return "var %s: %s := %s" %(decl.name, decl.type.accept(self), decl.exp.accept(self))
            else:
                if decl.escapes and self.semantics:
                    return "var %s/*e*/:= %s" %(decl.name, decl.exp.accept(self))   
                return "var %s:= %s" %(decl.name, decl.exp.accept(self))

        elif decl.exp is not None :
            if decl.escapes and self.semantics:
                return "var %s/*e*/ := %s" %(decl.name, decl.exp.accept(self))
            return "var %s := %s" %(decl.name, decl.exp.accept(self))

        else:
                return "%s: %s"%(decl.name, decl.type.accept(self))
        
    @visitor(FunDecl)
    def visit(self, funcDecl):

        n = len(funcDecl.args)
        args = ""

        for i in range(n):
            args += funcDecl.args[i].accept(self)

            if i!= n-1:
                args+=","
                
        if funcDecl.type is not None:
            if funcDecl.type.accept(self)!= "void":
                return "function %s(%s): %s = %s"%(funcDecl.name, args, funcDecl.type.accept(self), funcDecl.exp.accept(self))
            else:
                return "function %s(%s) = %s"%(funcDecl.name, args, funcDecl.exp.accept(self))

        return "function %s(%s) = %s" % (funcDecl.name, args, funcDecl.exp.accept(self))
    

    @visitor(FunCall)
    def visit(self, funCall):

        parameter = ""
        n = len(funCall.params)

        for i in range(n):
            parameter += funCall.params[i].accept(self)
            
            if i != n-1:
                parameter += ","

        return "%s(%s)"%(funCall.identifier.accept(self), parameter)                

    @visitor(Type)
    def visit(self, tp):
        return tp.typename
    
    @visitor(Identifier)
    def visit(self, id):
        
        if self.semantics and not isinstance(id.decl,FunDecl):
            
            diff = id.depth - id.decl.depth
            scope_diff = "/*%d*/" % diff if diff else ''
        else:
            scope_diff = ''
        return '%s%s' % (id.name, scope_diff)

    @visitor(IfThenElse)
    def visit(self,ifcond):
        if ifcond.else_part is None:
            return "if %s then %s"% (ifcond.condition.accept(self),ifcond.then_part.accept(self))
        return "if %s then %s else %s" % (ifcond.condition.accept(self),ifcond.then_part.accept(self),ifcond.else_part.accept(self))

    @visitor(While)
    def visit(self,whilecond):
        return "while %s do %s"%(whilecond.condition.accept(self), whilecond.exp.accept(self))

    @visitor(For)
    def visit(self, forcond):
        return "for %s := %s to %s do %s"% (forcond.indexdecl.accept(self), forcond.low_bound.accept(self), forcond.high_bound.accept(self), forcond.exp.accept(self))

    @visitor(IndexDecl)
    def visit(self, index):
        return index.name

    
    @visitor(SeqExp)
    def visit(self, sequence):
        
        seq = ""
        
        for i in range(len(sequence.exps)):
            seq += sequence.exps[i].accept(self)

            if i != len(sequence.exps) - 1:
                seq += ";"

        return "(%s)"%(seq)

    
    @visitor(Assignment)
    def visit(self, assign):
        
        return "%s := %s"%(assign.identifier.accept(self), assign.exp.accept(self))
