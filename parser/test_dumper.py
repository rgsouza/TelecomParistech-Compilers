#
# File provided by Compilers course TelecomParitech
# Code implemented by Rayanne Souza
# Last modification: 24 Oct 2015
#

import unittest

from parser.dumper import Dumper
from parser.parser import parse



class TestDumper(unittest.TestCase):

    def parse_dump(self, text):
        tree = parse(text)
        return tree.accept(Dumper(semantics=False))

    def check(self, text, expected):
        self.assertEqual(self.parse_dump(text), expected)

    def test_literal(self):
        self.check("42", "42")

    def test_priority(self):
        self.check("1+2*3", "(1 + (2 * 3))")
        self.check("2*3+1", "((2 * 3) + 1)")
        self.check("6-3*2","(6 - (3 * 2))")
        self.check("6/3-2","((6 / 3) - 2)")
        self.check("6/3-2*3+1","(((6 / 3) - (2 * 3)) + 1)")
        self.check("6-3*2","(6 - (3 * 2))")
        self.check("-1","(0 - 1)")
        self.check("-1-2*4","((0 - 1) - (2 * 4))")
        self.check("-6/3-2","(((0 - 6) / 3) - 2)")
        self.check("-(2+3-4)","(0 - ((2 + 3) - 4))")
            
        self.check("2*2-1>3*2+1","(((2 * 2) - 1) > ((3 * 2) + 1))")
        self.check("2*2+10<3*2+1","(((2 * 2) + 10) < ((3 * 2) + 1))")
        self.check("2*1+10/2<=3*2+1","(((2 * 1) + (10 / 2)) <= ((3 * 2) + 1))")
        self.check("2*1+10/2>=3*2+1","(((2 * 1) + (10 / 2)) >= ((3 * 2) + 1))")

        self.check("2*1+10/2<>3*2+1","(((2 * 1) + (10 / 2)) <> ((3 * 2) + 1))")
        self.check("2*1+10/2=3*2+1","(((2 * 1) + (10 / 2)) = ((3 * 2) + 1))")
        self.check("2>3*2-5&3<10/2+1","((2 > ((3 * 2) - 5)) & (3 < ((10 / 2) + 1)))")
        self.check("2>3*2-5|3<10/2+1","((2 > ((3 * 2) - 5)) | (3 < ((10 / 2) + 1)))")

        self.check("if 2>1 then 1 else 0","if (2 > 1) then 1 else 0")
        self.check("if 3*2>5 & 4<3 | 3*5>0 & 6*1 = 6 then 1 else 0", "if ((((3 * 2) > 5) & (4 < 3)) | (((3 * 5) > 0) & ((6 * 1) = 6))) then 1 else 0" )
        self.check("if if 4>3 | 0 then 1 else 0 then 3 else 4","if if ((4 > 3) | 0) then 1 else 0 then 3 else 4")

        self.check("for i := 0 to 10 do 1+2","for i := 0 to 10 do (1 + 2)")
        self.check("let function fact(n: int) = let var result := 1 in for i:= 1 to n do result := result*n; result end in fact(5) end","let function fact(n: int) = let var result := 1 in for i := 1 to n do result := (result * n); result end in fact(5) end")



    def test_decl(self):
        self.check("let var a:= 3 in a end","let var a := 3 in a end")
        self.check("let var a:int := 3 in a end","let var a: int := 3 in a end")
        self.check("let var a:= 3 var b := 5 in a end","let var a := 3 var b := 5 in a end")
        self.check("let var b:=4 var c:= 5 var d:=3 in a end","let var b := 4 var c := 5 var d := 3 in a end")
        self.check("let var a:= 2 function r()=4 in a end","let var a := 2 function r() = 4 in a end")
        self.check("let var a:= 2 function r():int=4 in a end","let var a := 2 function r(): int = 4 in a end")
        self.check("let var b:int :=2 function g():int=4 function r()=8 in a end","let var b: int := 2 function g(): int = 4 function r() = 8 in a end")
        self.check("let var a:= 2 function r():int=4 in r() end","let var a := 2 function r(): int = 4 in r() end")
        self.check("let var a: int:=3 var b:= a+1 function add(x:int):int=x in add((a + b)) end","let var a: int := 3 var b := (a + 1) function add(x: int): int = x in add((a + b)) end")
        self.check("let function f(a:int,b:int,c:int,d:int):int=a in f(a,b,c) end","let function f(a: int,b: int,c: int,d: int): int = a in f(a,b,c) end")
        self.check("let var a:int:=3 var b:= a+1 function add(x:int,y:int):int=x+y in add(a+b,3) end","let var a: int := 3 var b := (a + 1) function add(x: int,y: int): int = (x + y) in add((a + b),3) end")
        self.check("let var a:= 3 function f()= let function g()=a in g() end in f() end","let var a := 3 function f() = let function g() = a in g() end in f() end")
        self.check("let function f() = 1 function double(a: int) = a+a function g(c:int)=c in double(g(f())) end","let function f() = 1 function double(a: int) = (a + a) function g(c: int) = c in double(g(f())) end")
        self.check("let var a:= 2 function f(a:int):int=1 in f(a) end","let var a := 2 function f(a: int): int = 1 in f(a) end")

    def test_comment(self):
        self.check("//comment \n 1+2 ","(1 + 2)")
        self.check("//comment \n //comment \n 1+2","(1 + 2)")
        self.check("/*comment*/1+2","(1 + 2)")
        self.check("/*comment/*comment*/*/ 1+2","(1 + 2)")
        self.check("/*comment/*comment*/*/ let function f()=1 in f() end","let function f() = 1 in f() end")
        self.check("//comment \n let var a:=1 in a end","let var a := 1 in a end")

    def test_sequence(self):
        #self.check("(2+1;3+2)", "((2 + 1);(3 + 2))")
        #self.check("(1+2)", "(1 + 2)")
        self.check("let function f()=() in 0 end","let function f() = () in 0 end")
if __name__ == '__main__':
    unittest.main()
