#
# File provided by Compilers course from TelecomParitech
# Code implemented by Rayanne Souza
# Last modification: 23 Oct 2015
#

import unittest

from ast.evaluator import Evaluator
from ast.nodes import IntegerLiteral, BinaryOperator
from parser.parser import parse

class TestEvaluator(unittest.TestCase):

    def check(self, ast, expected):
        self.assertEqual(ast.accept(Evaluator()), expected)

    def parse_check(self, str, expected):
        self.assertEqual(parse(str).accept(Evaluator()), expected)

    def test_literal(self):
        self.check(IntegerLiteral(42), 42)

    def test_basic_operator(self):
        self.check(BinaryOperator('+', IntegerLiteral(10), IntegerLiteral(20)), 30)
        self.check(BinaryOperator('-', IntegerLiteral(50), IntegerLiteral(2)), 48)
        self.check(BinaryOperator('*', IntegerLiteral(10), IntegerLiteral(5)), 50)
        self.check(BinaryOperator('/', IntegerLiteral(50), IntegerLiteral(10)), 5)
        
    def test_priorities(self):
        self.check(BinaryOperator('+', IntegerLiteral(1), BinaryOperator('*', IntegerLiteral(2), IntegerLiteral(3))), 7)
        self.check(BinaryOperator('-', BinaryOperator('*', IntegerLiteral(5), IntegerLiteral(4)),IntegerLiteral(20)), 0) 
        self.check(BinaryOperator('-', BinaryOperator('/', IntegerLiteral(6), IntegerLiteral(2)),IntegerLiteral(1)), 2)

    def test_parse_literal(self):
        self.parse_check('42', 42)

    def test_parse_sequence(self):
        self.parse_check('1+(2+3)+4', 10)
        self.parse_check('6+(5-3)-1', 7 )
        self.parse_check('6-(3*2)+1', 1 )
        self.parse_check('(6/3)-2*(3+1)',-6)
        

    def test_precedence(self):
        self.parse_check('1 + 2 * 3', 7)
        self.parse_check('2 * 3 + 1', 7)
        self.parse_check('6 - 5*2', -4)
        self.parse_check('6/3 - 2*3',-4)
        self.parse_check('-1-2*4',-9)
        #self.parse_check('-3*-4/3',3)
        self.parse_check('2 * 2-1 > 3 * 2+1', 0)
        self.parse_check('2 * 2+10 >3 * 2+1', 1)
        self.parse_check('2 * 2 - 1 < 3 * 2 + 1', 1)
        self.parse_check('2 * 2 + 10 < 3 * 2 + 1', 0)

        self.parse_check('2 * 2 + 10/2 <= 3 * 2 + 1',0)
        self.parse_check('2 * 1 + 10/2 <= 3 * 2 + 1',1)
        self.parse_check('2 * 1 + 10/2 - 3<= 3 * 2 + 1',1)
        self.parse_check('2 * 2 + 10/2 >= 3 * 2 + 1',1)
        self.parse_check('2 * 1 + 10/2 >= 3 * 2 + 1',1)
        self.parse_check('2 * 1 + 10/2 - 1 >= 3 * 2 + 1',0)

        self.parse_check('2 * 1 + 10/2 <> 3 * 2 + 1',0)
        self.parse_check('2 * 2 + 10/2 + 1 <> 3 * 2 + 1',1)
        self.parse_check('2 * 1 + 10/2 = 3 * 2 + 1',1)
        self.parse_check('2 * 2 + 10/2 + 1 = 3 * 2 + 1',0)

        self.parse_check('2 < 3*2 - 5 & 3 < 10/2 + 1', 0)
        self.parse_check('2 > 3*2 - 5 & 3 < 10/2 + 1', 1)
        self.parse_check('2 <= 3*2 - 5 & 3 <= 10/2 + 1', 0)
        self.parse_check('2 >= 3*2 - 5 & 3 <= 10/2 + 1', 1)
        self.parse_check('2 <> 3*2 - 5 & 3 = 10/2 + 1', 0)

        self.parse_check('2 < 3*2 - 5 | 3 < 10/2 - 3', 0 )
        self.parse_check('2 > 3*2 - 5 | 3 > 10/2 - 3', 1 )
        self.parse_check('2 <= 3*2 - 5 | 3 <= 10/2 + 1', 1)
        self.parse_check('2 >= 3*2 - 5 | 3 <= 10/2 + 1', 1)
        self.parse_check('2 <> 3*2 - 5 | 3 = 10/2 + 1', 1)
        self.parse_check('if 3*9 - 5 >=2 | 3*5 + 4 <1 & 5=5 | 1>2 then 1 else 0', 1)

        

    def test_comparison(self):
        self.parse_check('2>3', 0)
        self.parse_check('3>2', 1)
        self.parse_check('2<3', 1)
        self.parse_check('3<2', 0)
        self.parse_check('2>=3', 0)
        self.parse_check('3>=2', 1)
        self.parse_check('2<=3', 1)
        self.parse_check('3<=2', 0)
        self.parse_check('3=2', 0)
        self.parse_check('2*4=8', 1)
        self.parse_check('3<>2', 1)
        self.parse_check('2*4<>8', 0)

    def test_conditional(self):
        self.parse_check('2 < 3 & 3 < 10', 1)
        self.parse_check('2 <= 3 & 3 <= 10', 1)
        self.parse_check('2 > 3 & 3 < 10', 0)
        self.parse_check('2 <= 3 & 3 >= 10', 0)
        self.parse_check('2 & 3', 1)
        self.parse_check('0 & 3', 0)
        self.parse_check('2 | 3', 1)
        self.parse_check('0 | 3', 1)
        self.parse_check('0 | 0', 0)

    def test_ifConditional(self):
        self.parse_check('if 2>1 then 1 else 0',1)
        self.parse_check('if 2*5 -1 > 2 & 3+4/2<=5 then 1 else 0', 1)
        self.parse_check('if if 4>3 | 0 then 1 else 0 then 3 else 4', 3)
        self.parse_check('if 3*2>5 & 4<3 | 3*5>0 & 6*1<>6 then 1 else 0', 0)
        self.parse_check('if 3*2>5 & 4<3 | 3*5>0 & 6*1=6 then 1 else 0', 1)

    def test_sequence(self):
        self.parse_check('(1; 2+3; 5+6)', 11)
        
        
if __name__ == '__main__':
    unittest.main()
