import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    def test0(self):
        """Simple program: class main {} """
        input = """class main {}"""
        expect = str(Program([ClassDecl(Id("main"),[])]))
        self.assertTrue(TestAST.test(input,expect,300))
    
    def test1(self):
        input = """class Shape{
            int main(){
                int x, y;
                final float z, y = 1e9, a = 1.0;
                string abc, xyz = 1;
            }
        }"""
        expect = str(
            Program(
                [ClassDecl(
                    Id("Shape"),
                    [MethodDecl(
                        Instance(),
                        Id("main"),
                        [],
                        IntType(),
                        Block(
                            [
                                VarDecl(Id("x"), IntType(), None),
                                VarDecl(Id("y"), IntType(), None),
                                ConstDecl(Id("z"), FloatType(), FloatLiteral(1e9)),
                                ConstDecl(Id("y"), FloatType(), FloatLiteral(1e9)),
                                ConstDecl(Id("a"), FloatType(), FloatLiteral(1.0)),
                                VarDecl(Id("abc"), StringType(), IntLiteral(1)),
                                VarDecl(Id("xyz"), StringType(), IntLiteral(1))
                            ],
                            [])
                    )]
                )]
            )
        )
        self.assertTrue(TestAST.test(input,expect,301))
    
    def test2(self):
        input = """class test{
            static void support(int f; float a, b, c; boolean x, y) {}
            int main(){}
        }"""
        expect = str(
            Program(
                [ClassDecl(
                    Id("test"),
                    [MethodDecl(
                        Static(),
                        Id("support"),
                        [VarDecl(Id("f"), IntType(), None),
                         VarDecl(Id("a"), FloatType(), None),
                         VarDecl(Id("b"), FloatType(), None),
                         VarDecl(Id("c"), FloatType(), None),
                         VarDecl(Id("x"), BoolType(), None),
                         VarDecl(Id("y"), BoolType(), None)
                         ],
                        VoidType(),
                        Block(
                            [],
                            []
                        )
                    ),
                    MethodDecl(
                        Instance(),
                        Id("main"),
                        [],
                        IntType(),
                        Block(
                            [], 
                            []
                        )
                    )
                    ]
                )]
            )
        )
        self.assertTrue(TestAST.test(input,expect,302))
    
    def test3(self):
        input = """class test{
            int x = 10, a;
        }
        """
        expect = str(
            Program(
                [ClassDecl(
                    Id("test"),
                    [
                    AttributeDecl(Instance(), VarDecl(Id("x"), IntType(), IntLiteral(10))),
                    AttributeDecl(Instance(), VarDecl(Id("a"), IntType(), None)),
                    ]
                )]
            )
        )
        self.assertTrue(TestAST.test(input, expect, 303))
        
    def test4(self):
        input = """class Test{
            int set(int val){
                x := -val;
                int x, y;
            }
        }
        """
        expect = str(
            Program(
                [ClassDecl(
                    Id("Test"),
                    [MethodDecl(
                        Instance(),
                        Id("set"),
                        [VarDecl(Id("val"), IntType(), None)],
                        IntType(),
                        Block(
                            [
                                VarDecl(Id("x"), IntType(), None),
                                VarDecl(Id("y"), IntType(), None)
                            ],
                            [
                                Assign(
                                    Id('x'),
                                    UnaryOp("-", Id("val"))
                                )
                            ]
                        )
                    )]
                )]
            )
        )
        self.assertTrue(TestAST.test(input, expect, 304))
    
    def test5(self):
        input = """class Test{
            int set(int val){
                int x, y;
                this.x := -val;
            }
        }
        """
        expect = str(
            Program(
                [ClassDecl(
                    Id("Test"),
                    [MethodDecl(
                        Instance(),
                        Id("set"),
                        [VarDecl(Id("val"), IntType(), None)],
                        IntType(),
                        Block(
                            [
                                VarDecl(Id("x"), IntType(), None),
                                VarDecl(Id("y"), IntType(), None)
                            ],
                            [
                                Assign(
                                    FieldAccess(SelfLiteral(), Id('x')),
                                    UnaryOp("-", Id('val'))
                                )
                            ]
                        )
                    )]
                )]
            )
        )
        self.assertTrue(TestAST.test(input, expect, 305))
    
    def test6(self):
        input = """class AttriTest{
            final int x = 10, a, b = 2.0, d = true;
            static int x, y = 10, z, f;
        }
        """
        expect = str(
            Program(
                [ClassDecl(
                    Id("AttriTest"),
                    [
                        AttributeDecl(
                            Instance(),
                            ConstDecl(Id("x"), IntType(), IntLiteral(10))
                        ),
                        AttributeDecl(
                            Instance(),
                            ConstDecl(Id("a"), IntType(), FloatLiteral(2.0))
                        ),
                        AttributeDecl(
                            Instance(),
                            ConstDecl(Id("b"), IntType(), FloatLiteral(2.0))
                        ),
                        AttributeDecl(
                            Instance(),
                            ConstDecl(Id("d"), IntType(), BooleanLiteral(True))
                        ),
                        AttributeDecl(
                            Static(),
                            VarDecl(Id("x"), IntType(), IntLiteral(10))
                        ),
                        AttributeDecl(
                            Static(),
                            VarDecl(Id("y"), IntType(), IntLiteral(10))
                        ),
                        AttributeDecl(
                            Static(),
                            VarDecl(Id("z"), IntType(), None)
                        ),
                        AttributeDecl(
                            Static(),
                            VarDecl(Id("f"), IntType())
                        )
                    ])
                ]
            )
        )
        self.assertTrue(TestAST.test(input, expect, 306))
    
    def test7(self):
        input = """class Example1{
            int factorial(int n){
                if n == 1 then return 1;
                else return n * this.factorial(n-1);
            }
        }
        """
        expect = str(
            Program(
                [ClassDecl(
                    Id("Example1"),
                    [MethodDecl(
                        Instance(),
                        Id("factorial"),
                        [VarDecl(Id("n"), IntType())],
                        IntType(),
                        Block(
                            [],
                            [
                                If(
                                    BinaryOp("==", Id("n"), IntLiteral(1)),
                                    Return(IntLiteral(1)),
                                    Return(
                                        BinaryOp("*",
                                                Id("n"),
                                                CallExpr(
                                                    SelfLiteral(),
                                                    Id("factorial"),
                                                    [
                                                        BinaryOp("-", Id("n"), IntLiteral(1))
                                                    ]
                                                )
                                                )
                                    )
                                )
                            ]
                        )
                    )]
                )]
            )
        )
        self.assertTrue(TestAST.test(input, expect, 307))
    
    def test8(self):
        input = """
        class Shape {
            float length,width;
            float getArea() {
                
            } 
            Shape(float length,width){
                this.length := length;
                this.width := width;
            }
        }
        class Rectangle extends Shape {
            float getArea(){
                return this.length*this.width;
            } 
        }
        class Triangle extends Shape { 
            float getArea(){
                return this.length*this.width / 2;
            }
        }
        class Example2 {
            void main(){ 
                s := new Rectangle(3,4); 
                io.writeFloatLn(s.getArea()); 
                s := new Triangle(3,4); 
                io.writeFloatLn(s.getArea());
            } 
        }
        """
        
        expect = str(
            Program(
                [
                    ClassDecl(
                        Id("Shape"),
                        [
                            AttributeDecl(
                                Instance(), 
                                VarDecl(Id("length"), FloatType())
                            ),
                            AttributeDecl(
                                Instance(),
                                VarDecl(Id("width"), FloatType())
                            ),
                            MethodDecl(
                                Instance(),
                                Id("getArea"),
                                [],
                                FloatType(),
                                Block(
                                    [],
                                    []
                                )
                            ),
                            MethodDecl(
                                Instance(),
                                Id("<init>"),
                                [
                                    VarDecl(Id("length"), FloatType()),
                                    VarDecl(Id("width"), FloatType())
                                ],
                                None,
                                Block(
                                    [],
                                    [
                                        Assign(
                                            FieldAccess(
                                                SelfLiteral(),
                                                Id("length")
                                            ),
                                            Id("length")
                                        ),
                                        Assign(
                                            FieldAccess(
                                                SelfLiteral(),
                                                Id("width")
                                            ),
                                            Id("width")
                                        )
                                    ]
                                )
                            ),
                        ]
                    ),
                    ClassDecl(
                        Id("Rectangle"),
                        [
                            MethodDecl(
                                Instance(),
                                Id("getArea"),
                                [],
                                FloatType(),
                                Block(
                                    [],
                                    [
                                        Return(
                                            BinaryOp(
                                                "*",
                                                FieldAccess(
                                                    SelfLiteral(),
                                                    Id("length")
                                                ),
                                                FieldAccess(
                                                    SelfLiteral(),
                                                    Id("width")
                                                )
                                            )
                                        )
                                    ]
                                )
                            )
                        ],
                        Id("Shape")
                    ),
                    ClassDecl(
                        Id("Triangle"),
                        [
                            MethodDecl(
                                Instance(),
                                Id("getArea"),
                                [],
                                FloatType(),
                                Block(
                                    [],
                                    [
                                        Return(
                                            BinaryOp(
                                                "/",
                                                BinaryOp(
                                                    "*",
                                                    FieldAccess(
                                                        SelfLiteral(),
                                                        Id("length")
                                                    ),
                                                    FieldAccess(
                                                        SelfLiteral(),
                                                        Id("width")
                                                    )
                                                ),
                                                IntLiteral(2)
                                            )
                                        )
                                    ]
                                )
                            )
                        ],
                        Id("Shape")
                    ),
                    ClassDecl(
                        Id("Example2"),
                        [
                            MethodDecl(
                                Instance(),
                                Id("main"),
                                [],
                                VoidType(),
                                Block(
                                    [
                                        # VarDecl(
                                        #     Id("s"),
                                        #     ClassType(Id("Shape"))
                                        # )
                                    ],
                                    [
                                        Assign(
                                            Id("s"),
                                            NewExpr(
                                                Id("Rectangle"),
                                                [
                                                    IntLiteral(3),
                                                    IntLiteral(4)
                                                ]
                                            )
                                        ),
                                        CallStmt(
                                            Id("io"),
                                            Id("writeFloatLn"),
                                            [
                                                CallExpr(
                                                    Id("s"),
                                                    Id("getArea"),
                                                    []
                                                )
                                            ]
                                        ),
                                        Assign(
                                            Id("s"),
                                            NewExpr(
                                                Id("Triangle"),
                                                [
                                                    IntLiteral(3),
                                                    IntLiteral(4)
                                                ]
                                            )
                                        ),
                                        CallStmt(
                                            Id("io"),
                                            Id("writeFloatLn"),
                                            [
                                                CallExpr(
                                                    Id("s"),
                                                    Id("getArea"),
                                                    []
                                                )
                                            ]
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ]
            )
        )
        self.assertTrue(TestAST.test(input, expect, 308))
    
    def test9(self):
        input = """
        class ArrayTest {
            final int[5] arr = {1,2,3,4,5};
            static float[1] ar = {1.0,2e2};
            Shape[10] sh;
        }
        """
        expect = str(
            Program(
                [
                    ClassDecl(
                        Id("ArrayTest"),
                        [
                            AttributeDecl(
                                Instance(),
                                ConstDecl(
                                    Id("arr"),
                                    ArrayType(5, IntType()),
                                    ArrayLiteral(
                                        [
                                            IntLiteral(1),
                                            IntLiteral(2),
                                            IntLiteral(3),
                                            IntLiteral(4),
                                            IntLiteral(5)
                                        ]
                                    )
                                )
                            ),
                            AttributeDecl(
                                Static(),
                                VarDecl(
                                    Id("ar"),
                                    ArrayType(1, FloatType()),
                                    ArrayLiteral(
                                        [
                                            FloatLiteral(1.0),
                                            FloatLiteral(2e2)
                                        ]
                                    )
                                )
                            ),
                            AttributeDecl(
                                Instance(),
                                VarDecl(
                                    Id("sh"),
                                    ArrayType(10, ClassType(Id("Shape"))),
                                    None
                                )
                            )
                        ]
                    )
                ]
            )
        )
        self.assertTrue(TestAST.test(input, expect, 309))
        
if __name__ == '__main__':
    unittest.main()