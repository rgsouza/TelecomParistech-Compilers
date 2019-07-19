#
# File provided by Compilers course TelecomParitech
# Code implemented by Rayanne Souza
# Last modification: 24 Oct 2015
#

import unittest

from semantics.binder import Binder
from parser.parser import parse
from parser.dumper import Dumper

class TestBinder(unittest.TestCase):

    def parse_binder(self, text):
        tree = parse(text)
        tree.accept(Binder())
        return tree.accept(Dumper(True))

    def check(self, text, expected):
        self.assertEqual(self.parse_binder(text), expected)

    def test_binder(self):
        self.check("let function fact(n:int)=if(n<3)then n else (n*fact(n-1)) in fact(5) end","let function fact(n: int) = if (n < 3) then n else (n * fact((n - 1))) in fact(5) end")
        self.check("let function f()=1 in f() end","let function f() = 1 in f() end")
        self.check("let var a:=2 function f(n:int)=n+1 in f(a) end","let var a := 2 function f(n: int) = (n + 1) in f(a) end")
        self.check("let var b := 3 var a: int := 4 function f() = let var c := a+b in c end in f() end","let var b/*e*/ := 3 var a/*e*/: int := 4 function f() = let var c := (a/*1*/ + b/*1*/) in c end in f() end") 
        self.check("let var a:=1 var b:int:=2 function c()=a function g()=b function f(x:int,y:int)=x+y in f(c(),g()) end","let var a/*e*/ := 1 var b/*e*/: int := 2 function c() = a/*1*/ function g() = b/*1*/ function f(x: int,y: int) = (x + y) in f(c(),g()) end")
        #self.check("let var a:=a in a end","let var a:=a in a end")
        self.check("let function fact(n: int) = let var result := 1 in for i:= 1 to n do result := result*n; result end in fact(5) end","let function fact(n: int) = let var result := 1 in for i := 1 to n do result := (result * n); result end in fact(5) end")
        self.check("let var a:=1 var b:=2 function f(n: int) = ( a; for i:= 1 to 10 do a:= a+1) in f(b) end ", "let var a/*e*/ := 1 var b := 2 function f(n: int) = (a/*1*/;for i := 1 to 10 do a/*1*/ := (a/*1*/ + 1)) in f(b) end")







if __name__ == '__main__':
    unittest.main()
