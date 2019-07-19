#
# File provided by Compilers course from TelecomParitech
# Code implemented by Rayanne Souza
# Last modification: 7 Oct 2015
#

import ply.lex as lex

# List of keywords. Each keyword will be return as a token of a specific
# type, which makes it easier to match it in grammatical rules.
keywords = {'array': 'ARRAY',
            'break': 'BREAK',
            'do': 'DO',
            'else': 'ELSE',
            'end': 'END',
            'for': 'FOR',
            'function': 'FUNCTION',
            'if': 'IF',
            'in': 'IN',
            'let': 'LET',
            'nil': 'NIL',
            'of': 'OF',
            'then': 'THEN',
            'to': 'TO',
            'type': 'TYPE',
            'var': 'VAR',
            'while': 'WHILE'}

# List of tokens that can be recognized and are handled by the current
# grammar rules.
tokens = ('END', 'IN', 'LET', 'VAR','TYPE',
          'FUNCTION','WHILE','DO','FOR','TO',
          'PLUS', 'TIMES',
          'COMMA', 'SEMICOLON',
          'LPAREN', 'RPAREN',
          'NUMBER', 'ID',
          'COLON', 'ASSIGN','MINUS','UMINUS',
	  'DIVISION','AND','OR','EQUAL',
	  'DIFFERENT','GTHAN','LTHAN','GETHAN',
	  'LETHAN', 'IF','THEN','ELSE')




t_PLUS = r'\+'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_ASSIGN = r':='
t_COMMA = r','
t_SEMICOLON = r';'
t_MINUS = r'\-'   
t_DIVISION = r'/'
t_AND = r'&'
t_OR = r'\|'
t_EQUAL = r'='
t_DIFFERENT = r'<>'
t_GTHAN = r'>'
t_LTHAN = r'<'
t_GETHAN = r'>='
t_LETHAN = r'<='


t_ignore = ' \t'

states = (('comment','exclusive'),
          )


# Count lines when newlines are encountered
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Distinguish between identifier and keyword. If the keyword is not also
# in the tokens list, this is a syntax error pure and simple since we do
# not know what to do about it.
def t_ID(t):
    r'[A-Za-z][A-Za-z\d_]*'
    if t.value in keywords:
        t.type = keywords.get(t.value)
        if t.type not in tokens:
            raise lex.LexError("unhandled keyword %s" % t.value, t.type)
    return t

# Recognize number - no leading 0 are allowed
def t_NUMBER(t):
    r'[1-9]\d*|0'
    t.value = int(t.value)
    return t

def t_comment(t):
    r'//.*'
    pass

def t_ANY_begin_comment(t):
    r'[/][*]'
    t.lexer.push_state('comment')
    pass

def t_comment_end(t):
    r'[*][/]'
    t.lexer.pop_state()

def t_comment_error(t):
    t.lexer.skip(1)

def t_error(t):
    raise lex.LexError("unknown token %s" % t.value, t.value)

lexer = lex.lex()
