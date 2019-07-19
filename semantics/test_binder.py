#
# File provided by Compilers course from TelecomParitech
# Code implemented by Rayanne Souza
# Last modification: 20 Oct 2015
#

import unittest

from semantics.binder import Binder
from parser.parser import parse

class TestBinder(unittest.TestCase):

    def parse_binder(self, text):
        tree = parse(text)
        return tree.accept(Binder())

    def check(self, text, expected):
        self.assertEqual(self.parse_binder(text), expected)

    def test_binder(self):
        self.check("let var b:= 3 var a: int:= 4 function g()=let var c= a+b in c end in f() end","") 
        self.check("let var a:= a in  end", "let var a:= a in a end")






if __name__ == '__main__':
    unittest.main()
