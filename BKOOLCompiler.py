from ply import lex, yacc
from AST import *

class BKOOLCompiler:
    def __init__(self):
        # Create lexer
        self.lexer = lex.lex(module=self)
        # Create parser
        self.parser = yacc.yacc(module=self)
        
    #!####################### LEXER RULES ########################
    # Token list
    tokens = (
        # Keywords
        'BOOLEAN', 'BREAK', 'CLASS', 'CONTINUE', 'DO', 
        'ELSE', 'EXTENDS', 'FLOAT', 'IF', 'INT', 'NEW', 
        'STRING', 'THEN', 'FOR', 'RETURN', 'TRUE', 'FALSE', 
        'VOID', 'NIL', 'THIS', 'FINAL', 'STATIC', 'TO', 'DOWNTO', 
        # Operators
        'ADD_OP', 'SUB_OP', 'MUL_OP', 'FLODIV_OP', 'INTDIV_OP',
        'MOD_OP', 'EQUAL_OP', 'NEQUAL_OP', 'LT_OP', 'GT_OP', 'LTE_OP',
        'GTE_OP', 'OR_OP', 'AND_OP', 'NOT_OP', 'CONCAT_OP', 'ASSIGN_OP', 
        'EQUAL_SIGN', 
        # Seperators
        'LSB', 'RSB', 'LP', 'RP', 'LB', 'RB', 'SEMI', 'COLON', 'DOT', 'COMMA', 
        # Atom
        'ID', 'INTLIT', 'FLOATLIT', 'STRINGLIT',
    )
    
    # Operator
    t_ADD_OP = r'\+'
    t_SUB_OP = r'-'
    t_MUL_OP = r'\*'
    t_FLODIV_OP = r'/'
    t_INTDIV_OP = r'\\'
    t_MOD_OP = r'%'
    t_EQUAL_OP = r'=='
    t_NEQUAL_OP = r'!='
    t_LT_OP = r'<'
    t_GT_OP = r'>'
    t_LTE_OP = r'<='
    t_GTE_OP = r'>='
    t_OR_OP = r'\|\|'
    t_AND_OP = r'&&'
    t_NOT_OP = r'!'
    t_CONCAT_OP = r'\^'
    t_ASSIGN_OP = r':='
    t_EQUAL_SIGN = r'='
    
    # Seperator
    t_LSB = r'\['
    t_RSB = r'\]'
    t_LP = r'{'
    t_RP = r'}'
    t_LB = r'\('
    t_RB = r'\)'
    t_SEMI = r';'
    t_COLON = r':'
    t_DOT = r'\.'
    t_COMMA = r','
    
    # IDENTIFIER
    def t_ID(self, t):
        r'[_a-zA-Z][_a-zA-Z0-9]*'
        t.type = self.reserved.get(t.value,'ID')
        return t
    
    # FLOATLIT
    def t_FLOATLIT(self, t):
        r'(\d+\.\d*[eE][-+]?\d+)|(\d+[eE][-+]?\d+)|(\d+\.\d*)'
        t.value = float(t.value)
        return t
    
    # INTLIT
    def t_INTLIT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # STRINGLIT
    def t_STRINGLIT(self, t):
        r'"([^"\\]|\\.)*"'
        t.value = t.value[1:-1]
        return t
    
    # Ignore space ( ) and tab (\t)
    t_ignore = ' \t'

    # Ignore in-line comment (#)
    def t_LINE_COMMENT(self, t):
        r'\#.*'
        pass

    # Ignore multi-line comment (/* ... */)
    def t_BLOCK_COMMENT(self, t):
        r'/\*(.|\n)*?\*/'
        pass

    # Error handling
    def t_error(self, t):
        print(f"Unable to recognize: '{t.value[0]}'")
        t.lexer.skip(1)
    
    # keyword list (reserved)
    reserved = {
        'boolean': 'BOOLEAN',
        'break': 'BREAK',
        'class': 'CLASS',
        'continue': 'CONTINUE',
        'do': 'DO',
        'else': 'ELSE',
        'extends': 'EXTENDS',
        'float': 'FLOAT',
        'if': 'IF',
        'int': 'INT',
        'new': 'NEW',
        'string': 'STRING',
        'then': 'THEN',
        'for': 'FOR',
        'return': 'RETURN',
        'true': 'TRUE',
        'false': 'FALSE',
        'void': 'VOID',
        'nil': 'NIL',
        'this': 'THIS',
        'final': 'FINAL',
        'static': 'STATIC',
        'to': 'TO',
        'downto': 'DOWNTO',
    }
    
    #!####################### PARSER RULES ########################
    # ~ 2.1: Class Declaration 
    def p_program(self, ctx):
        '''
        program : classDeclList
        '''
        ctx[0] = Program(ctx[1])
    
    def p_classDeclList(self, ctx):
        '''
        classDeclList : classDecl classDeclList 
                    | classDecl
        '''
        if (len(ctx) == 3): ctx[0] = ctx[1] + ctx[2]
        elif (len(ctx) == 2): ctx[0]=  ctx[1]
    
    def p_classDecl(self, ctx):
        '''
        classDecl : CLASS ID classExtends LP classMemberList RP
        '''
        ctx[0] = [ClassDecl(Id(ctx[2]), ctx[5], ctx[3])]
    
    def p_classExtends(self, ctx):
        '''
        classExtends : EXTENDS ID 
                    | empty
        '''
        if (len(ctx) == 3): ctx[0] = Id(ctx[2])
        else: ctx[0] = None

    def p_classMemberList(self, ctx):
        '''
        classMemberList : classMember classMemberList 
                        | empty
        '''
        if (len(ctx) == 3): ctx[0] = ctx[1] + ctx[2]
        else: ctx[0] = []
        
    def p_classMember(self, ctx):
        '''
        classMember : attrDecl 
                    | methodDecl
        '''
        ctx[0] = ctx[1]

    # ~ 2.2: Attribute Declaration 
    def p_attrDecl(self, ctx):
        '''
        attrDecl : immutDecl 
                | mutDecl
        '''
        ctx[0] = ctx[1]
    
    def p_immutDecl(self, ctx):
        '''
        immutDecl : FINAL typ attrList SEMI
                | STATIC FINAL typ attrList SEMI
                | FINAL STATIC typ attrList SEMI
        '''
        l = len(ctx)
        if (l == 5): kind = Instance()
        else: kind = Static()
        constdecl_list = [ConstDecl(y[0], ctx[l-3], y[1]) for x in ctx[l-2] for y in x] 
        ctx[0] = [AttributeDecl(kind, x) for x in constdecl_list]
        
    def p_mutDecl(self, ctx):
        '''
        mutDecl : STATIC typ attrList SEMI
                | typ attrList SEMI
        '''
        l = len(ctx)
        if (l == 5): kind = Static()
        else: kind = Instance()
        vardecl_list = [VarDecl(y[0], ctx[l-3], y[1]) for x in ctx[l-2] for y in x]
        ctx[0] = [AttributeDecl(kind, x) for x in vardecl_list]

    def p_attrList(self, ctx):
        '''
        attrList : attrMember COMMA attrList 
                | attrMember
        '''
        if (len(ctx) == 2): ctx[0] = [ctx[1]]
        else: ctx[0] = [ctx[1]] + ctx[3]
        
    def p_attrMember(self, ctx):
        '''
        attrMember : idlist attrInit
        '''
        ctx[0] = [[x, ctx[2]] for x in ctx[1]]
    
    def p_attrInit(self, ctx):
        '''
        attrInit : EQUAL_SIGN expr 
                | empty
        '''
        if (len(ctx) == 3): ctx[0] = ctx[2]
        else: ctx[0] = None
    
    # ~ 2.3: Method Declaration 
    def p_methodDecl(self, ctx):
        '''
        methodDecl : constructor
                    | normalMethod
        '''
        ctx[0] = ctx[1]
    
    def p_constructor(self, ctx):
        '''
        constructor : ID LB paramList RB blockstmt
        '''
        ctx[0] = [MethodDecl(Instance(), Id("<init>"), ctx[3], None, ctx[5])]
    
    def p_normalMethod(self, ctx):
        '''
        normalMethod : STATIC typ ID LB paramList RB blockstmt
                    | typ ID LB paramList RB blockstmt
        '''
        l = len(ctx)
        if (l == 8): kind = Static()
        else: kind = Instance()
        ctx[0] = [MethodDecl(kind, Id(ctx[l-5]), ctx[l-3], ctx[l-6], ctx[l-1])]
    
    def p_paramList_paramPrime(self, ctx):
        '''
        paramList : paramPrime 
        '''
        ctx[0] = ctx[1]
    
    def p_paramList_empty(self, ctx):
        '''
        paramList : empty
        '''
        ctx[0] = []
    
    def p_paramPrime(self, ctx):
        '''
        paramPrime : param SEMI paramPrime 
                | param
        '''
        if (len(ctx) == 2): ctx[0] = ctx[1]
        else: ctx[0] = ctx[1] + ctx[3]
    
    def p_param(self, ctx):
        '''
        param : typ idlist
        '''
        ctx[0] = [VarDecl(x, ctx[1], None) for x in ctx[2]]
    
    def p_idlist(self, ctx):
        '''
        idlist : ID COMMA idlist 
                | ID
        '''
        if (len(ctx) == 2): ctx[0] = [Id(ctx[1])]
        else: ctx[0] = [Id(ctx[1])] + ctx[3]
    
    # ~ 6: Statement 
    def p_stmtlist(self, ctx):
        '''
        stmtlist : stmt stmtlist 
                | empty
        '''
        if (len(ctx) == 3): ctx[0] = [ctx[1]] + ctx[2]
        else: ctx[0] = []
    
    def p_stmt(self, ctx):
        '''
        stmt : vardecllist
            |	blockstmt
            |	asmstmt
            |	ifstmt
            |	forstmt
            |	breakstmt
            |	contstmt
            |	retstmt
            |	methodivkstmt
        '''
        ctx[0] = ctx[1]
    
    def p_blockstmt(self, ctx):
        '''
        blockstmt : LP stmtlist RP
        '''
        stmt_visit_list = []
        
        stack = [ctx[2]]
        
        while stack:
            current = stack.pop()
            if isinstance(current, list):
                stack.extend(reversed(current))
            else:
                stmt_visit_list.append(current)
        
        decls = []
        stmts = []
        for stmt in stmt_visit_list:
            if isinstance(stmt, StoreDecl):
                decls.append(stmt)
            elif isinstance(stmt, Stmt):
                stmts.append(stmt)
        
        ctx[0] = Block(decls, stmts)
        
    def p_vardecl(self, ctx):
        '''
        vardecl : FINAL typ attrList SEMI 
                | typ attrList SEMI
        '''
        if (len(ctx) == 5): ctx[0] = [ConstDecl(y[0], ctx[2], y[1]) for x in ctx[3] for y in x]
        else: ctx[0] = [VarDecl(y[0], ctx[1], y[1]) for x in ctx[2] for y in x]

    def p_asmstmt(self, ctx):
        '''
        asmstmt : expr9 DOT ID ASSIGN_OP expr SEMI
                | expr8 ASSIGN_OP expr SEMI
        '''
        if (len(ctx) == 7): ctx[0] = Assign(FieldAccess(ctx[1], Id(ctx[3])), ctx[5])
        else: ctx[0] = Assign(ctx[1], ctx[3])
    
    def p_ifstmt(self, ctx):
        '''
        ifstmt : IF expr THEN stmt 
            | IF expr THEN stmt ELSE stmt
        '''
        if (len(ctx) == 7): elseStmt = ctx[6]
        else: elseStmt = None
        ctx[0] = If(ctx[2], ctx[4], elseStmt)
    
    def p_forstmt(self, ctx):
        '''
        forstmt : FOR ID ASSIGN_OP expr TO expr DO stmt
                | FOR ID ASSIGN_OP expr DOWNTO expr DO stmt
        '''
        up = True if ctx[5] == 'to' else False
        ctx[0] = For(Id(ctx[2]), ctx[4], ctx[6], up, ctx[8])
    
    def p_breakstmt(self, ctx):
        '''
        breakstmt : BREAK SEMI
        '''
        ctx[0] = Break()
    
    def p_contstmt(self, ctx):
        '''
        contstmt : CONTINUE SEMI
        '''
        ctx[0] = Continue()
    
    def p_retstmt(self, ctx):
        '''
        retstmt : RETURN expr SEMI
        '''
        ctx[0] = Return(ctx[2])
    
    def p_methodivkstmt(self, ctx):
        '''
        methodivkstmt : expr9 DOT ID LB arglist RB SEMI
        '''
        ctx[0] = CallStmt(ctx[1], Id(ctx[3]), ctx[5])
    
    def p_vardecllist(self, ctx):
        '''
        vardecllist : vardecl vardecllist
                    | vardecl
        '''
        if (len(ctx) == 3):
            ctx[0] = ctx[1] + ctx[2]
        else:
            ctx[0] = ctx[1]
    
    def p_expr(self, ctx):
        '''
        expr : expr1 GT_OP expr1
            | expr1 LT_OP expr1
            | expr1 GTE_OP expr1
            | expr1 LTE_OP expr1
            | expr1
        '''
        if (len(ctx) == 4): ctx[0] = BinaryOp(ctx[2], ctx[1], ctx[3])
        else: ctx[0] = ctx[1]        
        
    def p_expr1(self, ctx):
        '''
        expr1 : expr2 EQUAL_OP expr2 
            | expr2 NEQUAL_OP expr2
            | expr2
        '''
        if (len(ctx) == 4): ctx[0] = BinaryOp(ctx[2], ctx[1], ctx[3])
        else: ctx[0] = ctx[1]
    
    def p_expr2(self, ctx):
        '''
        expr2 : expr2 AND_OP expr3 
            | expr2 OR_OP expr3
            | expr3
        '''
        if (len(ctx) == 4): ctx[0] = BinaryOp(ctx[2], ctx[1], ctx[3])
        else: ctx[0] = ctx[1]
        
    def p_expr3(self, ctx):
        '''
        expr3 : expr3 ADD_OP expr4 
            | expr3 SUB_OP expr4
            | expr4
        '''
        if (len(ctx) == 4): ctx[0] = BinaryOp(ctx[2], ctx[1], ctx[3])
        else: ctx[0] = ctx[1]
        
    def p_expr4(self, ctx):
        '''
        expr4 : expr4 MUL_OP expr5 
            | expr4 INTDIV_OP expr5 
            | expr4 FLODIV_OP expr5 
            | expr4 MOD_OP expr5 
            | expr5
        '''
        if (len(ctx) == 4): ctx[0] = BinaryOp(ctx[2], ctx[1], ctx[3])
        else: ctx[0] = ctx[1]
    
    def p_expr5(self, ctx):
        '''
        expr5 : expr5 CONCAT_OP expr6 
            | expr6
        '''
        if (len(ctx) == 4): ctx[0] = BinaryOp(ctx[2], ctx[1], ctx[3])
        else: ctx[0] = ctx[1]
    
    def p_expr6(self, ctx):
        '''
        expr6 : NOT_OP expr6 
            | expr7
        '''
        if (len(ctx) == 3): ctx[0] = UnaryOp(ctx[1], ctx[2])
        else: ctx[0] = ctx[1]
    
    def p_expr7(self, ctx):
        '''
        expr7 : ADD_OP expr7 
            | SUB_OP expr7
            | expr8 
        '''
        if (len(ctx) == 3): ctx[0] = UnaryOp(ctx[1], ctx[2])
        else: ctx[0] = ctx[1]
        
    def p_expr8(self, ctx):
        '''
        expr8 : expr9 LSB expr RSB 
            | expr9
        '''
        if (len(ctx) == 5): ctx[0] = ArrayCell(ctx[1], ctx[3])
        else: ctx[0] = ctx[1]
        
    def p_expr9(self, ctx):
        '''
        expr9 : expr9 DOT ID 					
            | expr9 DOT ID LB arglist RB
            | expr10
        '''
        if (len(ctx) == 4): ctx[0] = FieldAccess(ctx[1], Id(ctx[3]))
        elif (len(ctx) == 7): ctx[0] = CallExpr(ctx[1], Id(ctx[3]), ctx[5])
        else: ctx[0] = ctx[1]
    
    def p_expr10(self, ctx):
        '''
        expr10 : NEW ID LB arglist RB 
            | expr11
        '''
        if (len(ctx) == 6): ctx[0] = NewExpr(Id(ctx[2]), ctx[4])
        else: ctx[0] = ctx[1]
    
    def p_expr_11_this(self, ctx):
        '''
        expr11 : THIS 
        '''
        ctx[0] = SelfLiteral()
    
    def p_expr_11_id(self, ctx):
        '''
        expr11 : ID 
        '''
        ctx[0] = Id(ctx[1])
    
    def p_expr_11_nil(self, ctx):
        '''
        expr11 : NIL 
        '''
        ctx[0] = NullLiteral()
    
    def p_expr_11_others(self, ctx):
        '''
        expr11 : primiLit 
                | arrayLit 
                | subexpr
        '''
        ctx[0] = ctx[1]

    def p_arglist_argprime(self, ctx):
        '''
        arglist : argprime 
        '''
        ctx[0] = ctx[1]
    
    def p_arglist_empty(self, ctx):
        '''
        arglist : empty 
        '''
        ctx[0] = []
        

    def p_argprime(self, ctx):
        '''
        argprime : expr COMMA argprime 
                | expr
        '''
        if (len(ctx) == 4):
            ctx[0] = [ctx[1]] + ctx[3]
        else:
            ctx[0] = [ctx[1]]
        
    def p_primiLit_intLit(self, ctx):
        '''
        primiLit : INTLIT
        '''
        ctx[0] = IntLiteral(ctx[1])
    
    def p_primiLit_floatLit(self, ctx):
        '''
        primiLit : FLOATLIT
        '''
        ctx[0] = FloatLiteral(ctx[1])
    
    def p_primiLit_stringLit(self, ctx):
        '''
        primiLit : STRINGLIT
        '''
        ctx[0] = StringLiteral(ctx[1])
    
    def p_primiLit_booleanLit(self, ctx):
        '''
        primiLit : booleanLit
        '''
        ctx[0] = ctx[1]
    
    def p_subexpr(self, ctx):
        '''
        subexpr : LB expr RB
        '''
        ctx[0] = ctx[2]
    
    def p_booleanLit(self, ctx):
        '''
        booleanLit : TRUE 
                    | FALSE
        '''
        if (ctx[1] == 'true'): ctx[0] = BooleanLiteral(True)
        else: ctx[0] = BooleanLiteral(False)
    
    def p_arrayLit(self, ctx):
        '''
        arrayLit : LP arrMemberList RP
        '''
        ctx[0] = ArrayLiteral(ctx[2])

    def p_arrMemberList(self, ctx):
        '''
        arrMemberList : primiLit COMMA arrMemberList 
                    | primiLit
        '''
        if (len(ctx) == 4): ctx[0] = [ctx[1]] + ctx[3]
        else: ctx[0] = [ctx[1]]
    
    # ~ 4. TYPE
    def p_typ_void(self, ctx):
        '''
        typ : VOID
        '''
        ctx[0] = VoidType()
    
    def p_typ_others(self, ctx):
        '''
        typ : primiTyp 
            | classTyp 
            | arrayTyp
        '''
        ctx[0] = ctx[1]
        
    def p_primiTyp_int(self, ctx):
        '''
        primiTyp : INT 
        '''
        ctx[0] = IntType()
    
    def p_primiTyp_float(self, ctx):
        '''
        primiTyp : FLOAT 
        '''
        ctx[0] = FloatType()
    
    def p_primiTyp_string(self, ctx):
        '''
        primiTyp : STRING 
        '''
        ctx[0] = StringType()
    
    def p_primiTyp_boolean(self, ctx):
        '''
        primiTyp : BOOLEAN 
        '''
        ctx[0] = BoolType()
    
    def p_classTyp(self, ctx):
        '''
        classTyp : ID
        '''
        ctx[0] = ClassType(Id(ctx[1]))

    def p_arrayTyp(self, ctx):
        '''
        arrayTyp : primiTyp LSB INTLIT RSB
                | classTyp LSB INTLIT RSB
        '''
        ctx[0] = ArrayType(int(ctx[3]), ctx[1])
    
    def p_empty(self, ctx):
        '''
        empty :
        '''
        pass
        
    #*####################### Lexer methods #######################
    def tokenize(self, input_string):
        self.lexer.input(input_string)
        tokens_list = []
        while True:
            tok = self.lexer.token()
            if not tok: break
            tokens_list.append(tok)
        return [(token.type, token.value) for token in tokens_list]
    
    #*####################### Parser methods ########################
    def parse(self, input_string):
        return self.parser.parse(input_string, lexer=self.lexer, debug=True)

def main():
    # Simple testcase for Lexer 
    input_lexer = "\"\"This is a string\" in a string\""
    tokens = BKOOLCompiler().tokenize(input_lexer)
    print(tokens)
    
    # Simple testcase for Parser
    input_parser = '''
    class Shape{
        int main(){
            int x, y;
            final float z, y = 19, a = 1.0;
            string abc, xyz = 1;
        }
    }
    '''
    ast = BKOOLCompiler().parse(input_parser)
    print(ast)

if __name__ == '__main__':
    main()
    
    