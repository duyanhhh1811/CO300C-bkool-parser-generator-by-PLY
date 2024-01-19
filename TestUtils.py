from BKOOLCompiler import BKOOLCompiler
import os

global bkoolCompiler 
bkoolCompiler = BKOOLCompiler()

class TestLexer:
    @staticmethod
    def test(input, expect, num):
        ans = bkoolCompiler.tokenize(input)
        res = ans == expect

        test_dir = os.path.join(os.path.dirname(__file__), 'test')
        os.makedirs(test_dir, exist_ok=True)
        filename = os.path.join(test_dir, f"{num}.txt")
        
        with open(filename, "w") as file:
            file.write(f"Case:\t#{num}\nResult:\t{res}\nInput:\t{input}\nExpect:\t{expect}\nAnswer:\t{ans}")
            file.write("\n")
            
        if not ans:
            print(ans)

        return res

class TestAST:
    @staticmethod
    def test(input, expect, num):
        ans = str(bkoolCompiler.parse(input))
        res = ans == expect
        
        test_dir = os.path.join(os.path.dirname(__file__), 'test')
        os.makedirs(test_dir, exist_ok=True)
        filename = os.path.join(test_dir, f"{num}.txt")
        
        with open(filename, "w") as file:
            file.write(f"Case:\t#{num}\nResult:\t{res}\nInput:\t{input}\nExpect:\t{expect}\nAnswer:\t{ans}")
            file.write("\n")
            
        if not ans:
            print(ans)

        return res
        
