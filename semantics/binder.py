from ast.nodes import *
from utils.visitor import *


class BindException(Exception):
    """Exception encountered during the binding phase."""
    pass


class Binder(Visitor):
    """The binder takes care of linking identifier uses to its declaration. If
    will also remember the depth of every declaration and every identifier,
    and mark a declaration as escaping if it is accessed from a greater depth
    than its definition.

    A new scope is pushed every time a let, function declaration or for loop is
    encountered. It is not allowed to have the same name present several
    times in the same scope.

    The depth is increased every time a function declaration is encountered,
    and restored afterwards.

    A loop node for break is pushed every time we start a for or while loop.
    Pushing None means that we are outside of break scope, which happens in the
    declarations part of a let."""

    def __init__(self):
        """Create a new binder with an initial scope for top-level
        declarations."""
        self.depth = 0
        self.scopes = []
        self.push_new_scope()
        self.break_stack = [None]
        


    @visitor(BinaryOperator)
    def visit(self, binop):
        binop.left.accept(self)
        binop.right.accept(self)
        self.visit_all(binop.children)
        
    @visitor(IfThenElse)
    def visit(self, cond):
        cond.condition.accept(self)
        cond.then_part.accept(self)
        if cond.else_part is not None:
            cond.else_part.accept(self)
        self.visit_all(cond.children)

    @visitor(While)
    def visit(self, whilecond):
        whilecond.condition.accept(self)
        whilecond.exp.accept(self)
        self.visit_all(whilecond.children)

    @visitor(For)
    def visit(self, loopFor):
        self.push_new_scope()
        self.add_binding( loopFor.indexdecl)

        loopFor.low_bound.accept(self)
        loopFor.high_bound.accept(self)
        loopFor.exp.accept(self)
        self.visit_all(loopFor.children)

        self.pop_scope()    

    
        
    @visitor(Identifier)
    def visit(self, id):
        self.lookup(id)
        
        
    @visitor(Let)
    def visit(self, let):
        
        self.push_new_scope()
        self.visit_all(let.children)
        self.pop_scope()
            
    @visitor(FunDecl)
    def visit(self, funcDecl):
        self.depth +=1
        self.add_binding(funcDecl)
        self.push_new_scope()
        
    
        n = len(funcDecl.args)
        for i in range(n):
            funcDecl.args[i].accept(self)
           
        funcDecl.exp.accept(self)

        self.depth -=1
        self.pop_scope()
     
    @visitor(VarDecl)
    def visit(self, varDecl):
        
        self.add_binding( varDecl )

        if varDecl.exp is not None:
            
            if isinstance(varDecl.exp,Identifier):
        
                if varDecl.name != varDecl.exp.name:
                    return varDecl.exp.accept(self)
                else:
                    raise BindException("Expression error")
            else:
                return varDecl.exp.accept(self)
                

    @visitor(FunCall)
    def visit(self, funCall):
        
        decl = self.lookup(funCall.identifier)

        if isinstance(decl,FunDecl):
            self.visit_all(funCall.children)
            
            if len(decl.args) != len(funCall.params):
                raise BindException("Wrong number of parameters")
        
        else:
            raise BindException("It is not a function call")
        

    @visitor(Assignment)
    def visit(self, assign):
        decl = self.lookup(assign.identifier)
        
        if isinstance(decl, VarDecl):
            self.visit_all(assign.children)
        else:
            raise BindException("It is not a VarDecl")
        

    @visitor(SeqExp)
    def visit(self, seq):
        self.visit_all(seq.children)

    


    def push_new_scope(self):
        """Push a new scope on the scopes stack."""
        self.scopes.append({})

    def pop_scope(self):
        """Pop a scope from the scopes stack."""
        del self.scopes[-1]

    def current_scope(self):
        """Return the current scope."""
        return self.scopes[-1]

    def push_new_loop(self, loop):
        """Push a new loop node on the break stack."""
        self.break_stack.append(loop)

    def pop_loop(self):
        """Pop a loop node from the break stack."""
        del self.break_stack[-1]

    def current_loop(self):
        loop = self.break_stack[-1]
        if loop is None:
            raise BindException("break called outside of loop")

    def add_binding(self, decl):
        """Add a binding to the current scope and set the depth for
        this declaration. If the name already exists, an exception
        will be raised."""
        if decl.name in self.current_scope():
            raise BindException("name already defined in scope: %s" %
                                decl.name)
        self.current_scope()[decl.name] = decl
        decl.depth = self.depth

    def lookup(self, identifier):
        """Return the declaration associated with a identifier, looking
        into the closest scope first. If no declaration is found,
        raise an exception. If it is found, the decl and depth field
        for this identifier are set, and the escapes field of the
        declaration is updated if needed."""
        name = identifier.name
        
        for scope in reversed(self.scopes):
            if name in scope:
                decl = scope[name]
                identifier.decl = decl
                identifier.depth = self.depth
                decl.escapes |= self.depth > decl.depth
                
                return decl
        else:
            raise BindException("name not found: %s" % name)
