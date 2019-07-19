#
# File provided by Compilers course TelecomParitech
# Code implemented by Rayanne Souza
# Last modification: 2 Oct 2015
#

import unittest

from ply.lex import LexError

from .tokenizer import lexer

class TestLexer(unittest.TestCase):

    def check(self, type, value):
        t = lexer.token()
        self.assertEqual(t.type, type)
        self.assertEqual(t.value, value)

    def check_end(self):
        t = lexer.token()
        self.assertIsNone(t)

    def test_basic(self):
        lexer.input("42")
        self.check('NUMBER', 42)
        self.check_end()

    def test_op(self):
        lexer.input("1 + 2 * 3 > 0")
        self.check('NUMBER', 1)
        self.check('PLUS', '+')
        self.check('NUMBER', 2)
        self.check('TIMES', '*')
        self.check('NUMBER', 3)
        self.check('GTHAN','>')
        self.check('NUMBER', 0)
        self.check_end()

    def test_opLessThan(self):
        lexer.input("1 - 5 * 3 < 0")
        self.check('NUMBER', 1)
        self.check('MINUS', '-')
        self.check('NUMBER', 5)
        self.check('TIMES', '*')
        self.check('NUMBER', 3)
        self.check('LTHAN','<')
        self.check('NUMBER', 0)
        self.check_end()

    def test_opCMP(self):
        lexer.input("3 >= 2 & 1 <= 2 ")
        self.check('NUMBER', 3)
        self.check('GETHAN', '>=')
        self.check('NUMBER', 2)
        self.check('AND', '&')
        self.check('NUMBER', 1)
        self.check('LETHAN','<=')
        self.check('NUMBER', 2 )
        self.check_end()

    def test_opOr(self):
        lexer.input("3 >= 2 | 1 <= 2 ")
        self.check('NUMBER', 3)
        self.check('GETHAN', '>=')
        self.check('NUMBER', 2)
        self.check('OR', '|')
        self.check('NUMBER', 1)
        self.check('LETHAN','<=')
        self.check('NUMBER', 2 )
        self.check_end()        

    def test_opEgualandDiff(self):
        lexer.input("3 = 2 & 1 <> 2 ")
        self.check('NUMBER', 3)
        self.check('EQUAL', '=')
        self.check('NUMBER', 2)
        self.check('AND', '&')
        self.check('NUMBER', 1)
        self.check('DIFFERENT','<>')
        self.check('NUMBER', 2 )
        self.check_end()

    def test_opDivision(self):
        lexer.input("3 / 2")
        self.check('NUMBER', 3)
        self.check('DIVISION','/')
        self.check('NUMBER', 2)
        self.check_end()

    def test_if(self):
        lexer.input("if 3*2>0 | 0 then 1 else 0 ")
        self.check('IF','if')
        self.check('NUMBER', 3)
        self.check('TIMES', '*')
        self.check('NUMBER', 2)
        self.check('GTHAN','>')
        self.check('NUMBER', 0)
        self.check('OR', '|')
        self.check('NUMBER', 0)
        self.check('THEN', 'then')
        self.check('NUMBER', 1)
        self.check('ELSE', 'else')
        self.check('NUMBER', 0)
        self.check_end()

    def test_opAssing(self):
        lexer.input("var a , var b := (1, 2);")
        self.check('VAR', 'var')
        self.check('ID', 'a')
        self.check('COMMA',',')
        self.check('VAR', 'var')
        self.check('ID', 'b')
        self.check('ASSIGN',':=')
        self.check('LPAREN','(')
        self.check('NUMBER', 1)
        self.check('COMMA',',')
        self.check('NUMBER', 2)
        self.check('RPAREN',')')
        self.check('SEMICOLON',';')
        self.check_end()
        
    def test_keyword(self):
        lexer.input("var")
        self.check('VAR', 'var')
        self.check_end()

    def test_identifier(self):
        lexer.input("foobar")
        self.check('ID', 'foobar')
        self.check_end()

    def test_error(self):
        lexer.input("foobar@")
        self.check('ID', 'foobar')
        self.assertRaises(LexError, lexer.token)

    def test_unhandled_keyword(self):
        lexer.input("array")
        self.assertRaises(LexError, lexer.token)

if __name__ == '__main__':
    unittest.main()
