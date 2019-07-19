#
# File provided by Compilers course from TelecomParitech
# Code implemented by Rayanne Souza
# Last modification: 23 Oct 2015
#


from ast.nodes import *
from . import tokenizer
import ply.yacc as yacc

tokens = tokenizer.tokens
keyWords = tokenizer.keywords

precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','GETHAN','LETHAN','EQUAL','GTHAN','LTHAN','DIFFERENT'),
    ('left', 'PLUS','MINUS'),
    ('left', 'TIMES','DIVISION'),
    ('right','UMINUS'),

)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVISION expression
                  | expression GETHAN expression
                  | expression LETHAN expression
                  | expression EQUAL expression
                  | expression DIFFERENT expression
                  | expression GTHAN expression
                  | expression LTHAN expression
                  | expression AND expression
                  | expression OR expression'''

    p[0] = BinaryOperator(p[2], p[1], p[3])

   
def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''

    p[0] = BinaryOperator(p[1], IntegerLiteral(0),p[2]) 


def p_expression_ifThenElse(p):
    '''expression : IF expression THEN expression ELSE expression
                  | IF expression THEN expression'''
    if len(p) == 7:
        p[0] = IfThenElse(p[2], p[4],p[6])

    else:
        p[0] = IfThenElse(p[2], p[4], None)


def p_expression_while(p):
    'expression : WHILE expression DO expression'

    p[0] = While(p[2],p[4])

def p_expression_for(p):
    'expression : FOR ID ASSIGN expression TO expression DO expression'

    p[0] = For(IndexDecl(p[2]),p[4],p[6],p[8])
    
def p_expression_letIn(p):
    '''expression : LET decls IN sequence END'''


                 # | LET decls IN END
    if len(p) == 6:
        p[0] = Let(p[2], p[4])
    #else:
        #p[0] =  Let(p[2], [])

def p_decls(p):
    '''decls : decl
             | decls decl'''

    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]
        

def p_decl_varDecl(p):
    '''decl : VAR ID ASSIGN expression
            | VAR ID COLON ID ASSIGN expression'''

    if len(p) == 5:
        p[0] = VarDecl(p[2], None, p[4])

    elif len(p) == 7:
        p[0] = VarDecl(p[2], Type(p[4]), p[6])


def p_parameters(p):
    '''parameters :
                  | param
                  | parameters COMMA param'''

    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p)==4 and p[1] is not None and len(p[1])!= 0:
        p[0] = p[1]+ [p[3]]


def p_param(p):
    'param : ID COLON ID'

    if len(p) == 4:
        p[0] = VarDecl(p[1], Type(p[3]), None )
    
    

def p_decl_funDecl(p):
    '''decl : FUNCTION ID LPAREN parameters RPAREN EQUAL expression
            | FUNCTION ID LPAREN parameters RPAREN COLON ID EQUAL expression'''
    

    if len(p) == 8:
        p[0] = FunDecl(p[2], p[4], None,p[7])

    elif len(p) == 10:
        typename = Type(p[7])
        p[0] = FunDecl(p[2], p[4], typename, p[9])
        


def p_parameters_funCall(p):
    '''paramscall :
                  | paramcall
                  | paramscall COMMA paramcall '''

    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p)==4 and p[1] is not None and len(p[1])!= 0:
        p[0] = p[1]+ [p[3]]

def p_parameter_funCall(p):
    '''paramcall : expression'''
    p[0] = p[1]
    
def p_funCall(p):
    'expression : ID LPAREN paramscall RPAREN'

    p[0] = FunCall(Identifier(p[1]), p[3])
    
def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_sequence(p):
    '''sequence :
                | expression
                | sequence SEMICOLON expression'''

    if len(p) == 1:
        p[0] = []

    elif len(p) == 2:
        p[0] = [p[1]]

    elif p[1] is not None and len(p[1]) != 0:
        p[0] = p[1] + [p[3]]
        
def p_seq_expression(p):
    'expression : LPAREN sequence RPAREN'
    p[0] = SeqExp(p[2])

def p_expression_assignment(p):
    'expression : ID ASSIGN expression'

    p[0] = Assignment(Identifier(p[1]), p[3])

    
def p_expression_number(p):
    'expression : NUMBER'
    p[0] = IntegerLiteral(p[1])

def p_expression_identifier(p):
    'expression : ID'
    p[0] = Identifier(p[1])

def p_error(p):
    import sys
    sys.stderr.write("no way to analyze %s\n" % p)
    sys.exit(1)

parser = yacc.yacc()

def parse(text):
    return parser.parse(text, lexer = tokenizer.lexer.clone())
