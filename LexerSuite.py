import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):
    def test_case_0(self):
        input = "int x := 42; float y := 3.14;"
        expect = [
            ('INT', 'int'), ('ID', 'x'), ('ASSIGN_OP', ':='), ('INTLIT', 42),
            ('SEMI', ';'), ('FLOAT', 'float'), ('ID', 'y'), ('ASSIGN_OP', ':='),
            ('FLOATLIT', 3.14), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 0))
    
    def test_case_1(self):
        input = "int x := 42;"
        expect = [
            ('INT', 'int'), ('ID', 'x'), 
            ('ASSIGN_OP', ':='), ('INTLIT', 42), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 1))

    def test_case_2(self):
        input = "float y = 3.14;"
        expect = [
            ('FLOAT', 'float'), ('ID', 'y'), 
            ('EQUAL_SIGN', '='), ('FLOATLIT', 3.14), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 2))

    def test_case_3(self):
        input = "boolean flag = true;"
        expect = [
            ('BOOLEAN', 'boolean'), ('ID', 'flag'), 
            ('EQUAL_SIGN', '='), ('TRUE', 'true'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 3))

    def test_case_4(self):
        input = "string s = \"Hello\";"
        expect = [
            ('STRING', 'string'), ('ID', 's'), 
            ('EQUAL_SIGN', '='), ('STRINGLIT', 'Hello'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 4))

    def test_case_5(self):
        input = "x + y - z;"
        expect = [
            ('ID', 'x'), ('ADD_OP', '+'), 
            ('ID', 'y'), ('SUB_OP', '-'), 
            ('ID', 'z'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 5))

    def test_case_6(self):
        input = "if (x > 0) {}"
        expect = [
            ('IF', 'if'), ('LB', '('), ('ID', 'x'), ('GT_OP', '>'), 
            ('INTLIT', 0), ('RB', ')'), ('LP', '{'), ('RP', '}')
        ]
        self.assertTrue(TestLexer.test(input, expect, 6))

    def test_case_7(self):
        input = "for i := 0 to 10 do {}"
        expect = [
            ('FOR', 'for'), ('ID', 'i'), ('ASSIGN_OP', ':='), 
            ('INTLIT', 0), ('TO', 'to'), ('INTLIT', 10), 
            ('DO', 'do'), ('LP', '{'), ('RP', '}')
        ]
        self.assertTrue(TestLexer.test(input, expect, 7))

    def test_case_8(self):
        input = "/* Comment */ x := 1;"
        expect = [
            ('ID', 'x'), ('ASSIGN_OP', ':='), ('INTLIT', 1), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 8))

    def test_case_9(self):
        input = "x = y == z;"
        expect = [
            ('ID', 'x'), ('EQUAL_SIGN', '='), ('ID', 'y'), 
            ('EQUAL_OP', '=='), ('ID', 'z'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 9))

    def test_case_10(self):
        input = "return x;"
        expect = [
            ('RETURN', 'return'), ('ID', 'x'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 10))
    
    def test_case_11(self):
        input = "class Example {}"
        expect = [
            ('CLASS', 'class'), ('ID', 'Example'), ('LP', '{'), ('RP', '}')
        ]
        self.assertTrue(TestLexer.test(input, expect, 11))

    def test_case_12(self):
        input = "void main() {}"
        expect = [
            ('VOID', 'void'), ('ID', 'main'), ('LB', '('), 
            ('RB', ')'), ('LP', '{'), ('RP', '}')
        ]
        self.assertTrue(TestLexer.test(input, expect, 12))

    def test_case_13(self):
        input = "x = y + 3;"
        expect = [
            ('ID', 'x'), ('EQUAL_SIGN', '='), ('ID', 'y'), 
            ('ADD_OP', '+'), ('INTLIT', 3), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 13))

    def test_case_14(self):
        input = "if (x < 10) {}"
        expect = [
            ('IF', 'if'), ('LB', '('), ('ID', 'x'), ('LT_OP', '<'), 
            ('INTLIT', 10), ('RB', ')'), ('LP', '{'), ('RP', '}')
        ]
        self.assertTrue(TestLexer.test(input, expect, 14))

    def test_case_15(self):
        input = "for (i = 0; i < 10; i++) {}"
        expect = [
            ('FOR', 'for'), ('LB', '('), ('ID', 'i'), ('EQUAL_SIGN', '='), 
            ('INTLIT', 0), ('SEMI', ';'), ('ID', 'i'), ('LT_OP', '<'), 
            ('INTLIT', 10), ('SEMI', ';'), ('ID', 'i'), ('ADD_OP', '+'), 
            ('ADD_OP', '+'), ('RB', ')'), ('LP', '{'), ('RP', '}')
        ]
        self.assertTrue(TestLexer.test(input, expect, 15))

    def test_case_16(self):
        input = "return 0;"
        expect = [
            ('RETURN', 'return'), ('INTLIT', 0), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 16))

    def test_case_17(self):
        input = "\"This is a string\""
        expect = [
            ('STRINGLIT', 'This is a string')
        ]
        self.assertTrue(TestLexer.test(input, expect, 17))

    def test_case_18(self):
        input = "# This is a comment\nx = 1;"
        expect = [
            ('ID', 'x'), ('EQUAL_SIGN', '='), ('INTLIT', 1), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 18))

    def test_case_19(self):
        input = "y *= 5;"
        expect = [
            ('ID', 'y'), ('MUL_OP', '*'), ('EQUAL_SIGN', '='), ('INTLIT', 5), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 19))

    def test_case_20(self):
        input = "boolean check = false;"
        expect = [
            ('BOOLEAN', 'boolean'), ('ID', 'check'), 
            ('EQUAL_SIGN', '='), ('FALSE', 'false'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 20))

    def test_case_21(self):
        input = "array[10];"
        expect = [
            ('ID', 'array'), ('LSB', '['), ('INTLIT', 10), ('RSB', ']'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 21))

    def test_case_22(self):
        input = "x++; y--;"
        expect = [
            ('ID', 'x'), ('ADD_OP', '+'), ('ADD_OP', '+'), ('SEMI', ';'), 
            ('ID', 'y'), ('SUB_OP', '-'), ('SUB_OP', '-'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 22))

    def test_case_23(self):
        input = "int[] arr = new int[10];"
        expect = [
            ('INT', 'int'), ('LSB', '['), ('RSB', ']'),
            ('ID', 'arr'), ('EQUAL_SIGN', '='), ('NEW', 'new'), 
            ('INT', 'int'), ('LSB', '['), ('INTLIT', 10), ('RSB', ']'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 23))

    def test_case_24(self):
        input = "break;"
        expect = [
            ('BREAK', 'break'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 24))

    def test_case_25(self):
        input = "continue;"
        expect = [
            ('CONTINUE', 'continue'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 25))

    def test_case_26(self):
        input = "x != y;"
        expect = [
            ('ID', 'x'), ('NEQUAL_OP', '!='), ('ID', 'y'), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 26))

    def test_case_27(self):
        input = "\"Escape \\n character\""
        expect = [
            ('STRINGLIT', 'Escape \\n character')
        ]
        self.assertTrue(TestLexer.test(input, expect, 27))

    def test_case_28(self):
        input = "x := 2;"
        expect = [
            ('ID', 'x'), ('ASSIGN_OP', ':='), ('INTLIT', 2), ('SEMI', ';')
        ]
        self.assertTrue(TestLexer.test(input, expect, 28))

if __name__ == '__main__':
    unittest.main()
