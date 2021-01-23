from lexer import Token, Tokenizer
from sly import Parser
from utils import error_message

class OneParser(Parser):
    tokens = Tokenizer.tok

    debugfile = 'parser.out'
    
    precedence = (('left', ADD, SUB),
                  ('left', MULT, DIV),
                  ('right', "LESS_THAN", "GREAT_THAN"),
                  ("left", "AND", "OR"),
                  ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = {}
        self.scope = "global"
        self.raw_prog = None

    
    @_("")
    def program(self, p):
        pass

    @_("statement")
    def program(self, p):
        return ("program", p.statement, None)


    @_("statement SEMI program")
    def program(self, p):
        return("program", p.program, p.statement)


    @_("FUNC_DEF IDENTIFIER COLON program BLOCK_END")
    def statement(self, p):
        return("func_def_void", p.IDENTIFIER, p.program, p)

    @_("FUNC_DEF IDENTIFIER SUB GREAT_THAN f_args COLON program BLOCK_END")
    def statement(self, p):
        return("func_def_args", p.IDENTIFIER, p.f_args, p.program, p)

    @_("IF expression COLON program BLOCK_END")
    def statement(self, p):
        return ("if_statement", p.expression, p.program, p)

    @_("IF  expression COLON program ELSE COLON program BLOCK_END")
    def statement(self, p):
        return ("if_else_statement", p.expression, p.program0, p.program1, p)

    @_("WHILE expression COLON program BLOCK_END")
    def statement(self, p):
        return ("while_setup", p.expression, p.program), p

    @_('FOR IDENTIFIER IN expression COLON program BLOCK_END')
    def statement(self, p):
        return ('for_loop', p.IDENTIFIER, p.expression, p.program, p)

    @_("RETURN expression")
    def statement(self, p):
        return ("return_stack", p.expression, p)

    @_("IDENTIFIER L_BRACE elements R_BRACE")
    def expression(self, p):
        return ("func_call", p.IDENTIFIER, p.elements, p)


    @_("DECLARATION IDENTIFIER ASSIGN statement")
    def statement(self, p):
        return ("var_decl_dynamic", p.IDENTIFIER, p.statement, p)

    @_("IDENTIFIER ASSIGN expression")
    def statement(self, p):
        return ("var_re_assign", p.IDENTIFIER, p.expression, p)

    @_("DECLARATION IDENTIFIER ASSIGN L_SQBRACE elements R_SQBRACE")
    def statement(self, p):
        return ("array_decl", p.IDENTIFIER, p.elements, p)

    @_("IDENTIFIER ASSIGN L_SQBRACE elements R_SQBRACE")
    def statement(self, p):
        return ("array_re_assign", p.IDENTIFIER, p.elements, p)

    @_("STRUCT IDENTIFIER COLON f_args SEMI BLOCK_END")
    def statement(self, p):
        return ("struct_def", p.IDENTIFIER, p.f_args, p)

    @_("IDENTIFIER L_SQBRACE expression R_SQBRACE")
    def expression(self, p):
        return ("element_access", p.IDENTIFIER, p.expression, p)

    @_("IDENTIFIER L_CURLY elements R_CURLY")
    def expression(self, p):
        return ("struct_assign", p.IDENTIFIER, p.elements, p)

    @_("IDENTIFIER DOT IDENTIFIER")
    def expression(self,p):
        return ("struct_element_access", p.IDENTIFIER0, p.IDENTIFIER1, p)

    @_("IDENTIFIER DOT IDENTIFIER SUB GREAT_THAN expression")
    def expression(self,p):
        return ("struct_element_reassign", p.IDENTIFIER0, p.IDENTIFIER1, p.expression, p)

    @_("expression")
    def statement(self, p):
        return p.expression

    @_("")
    def f_args(self, p):
        return []


    @_("DECLARATION IDENTIFIER")
    def f_args(self, p):
        return [p.IDENTIFIER]

    @_('f_args COMMA DECLARATION IDENTIFIER')
    def f_args(self, p):
        p.f_args.append(p.IDENTIFIER)
        return p.f_args

    @_("")
    def elements(self, p):
        return []

    @_("IDENTIFIER")
    def elements(self, p):
        return [("var", p.IDENTIFIER)]

    @_("literal")
    def elements(self, p):
        return [p.literal]
    
    @_("expression")
    def elements(self, p):
        return [("expr", p.expression)]

    @_('elements COMMA elements')
    def elements(self, p):
        return p.elements0 + p.elements1
        

    @_("INT")
    def literal(self, p):
        return p.INT

    @_("STRING")
    def literal(self, p):
        return p.STRING

    @_("FLOAT")
    def literal(self, p):
        return p.FLOAT
    
   
    @_("literal")
    def expression(self, p):
        return p.literal

    @_("IDENTIFIER")
    def literal(self, p):
        return ("var", p.IDENTIFIER)

    @_("L_BRACE expression R_BRACE")
    def expression(self, p):
        return p.expression


    @_("expression ADD expression")
    def expression(self, p):
        return("arithmetic", "add", p.expression0, p.expression1, p)

    @_("expression MOD expression")
    def expression(self, p):
        return("arithmetic", "mod", p.expression0, p.expression1, p)

    @_("expression SUB expression")
    def expression(self, p):
        return("arithmetic", "minus", p.expression0, p.expression1, p)

    @_(" expression DIV expression")
    def expression(self, p):
        return("arithmetic", "div", p.expression0, p.expression1, p)

    @_("expression MULT expression")
    def expression(self, p):
        return("arithmetic", "mult", p.expression0, p.expression1, p)

    @_("L_BRACE expression OR expression R_BRACE")
    def expression(self, p):
        return("compare", "or", p.expression0, p.expression1, p)

    @_("L_BRACE expression AND AND expression R_BRACE")
    def expression(self, p):
        return("compare", "and", p.expression0, p.expression1, p)

    @_("L_BRACE expression GREAT_THAN expression R_BRACE")
    def expression(self, p):
        return("compare", "greater", p.expression0, p.expression1, p)

    @_("L_BRACE expression LESS_THAN expression R_BRACE")
    def expression(self, p):
        return("compare", "lesser", p.expression0, p.expression1, p)

    @_("L_BRACE expression ASSIGN ASSIGN expression R_BRACE")
    def expression(self, p):
        return("compare", "equal", p.expression0, p.expression1, p)

    @_("L_BRACE expression NOT ASSIGN expression R_BRACE")
    def expression(self, p):
        return("compare", "notequal", p.expression0, p.expression1, p)

    @_("L_BRACE expression GREAT_THAN ASSIGN expression R_BRACE")
    def expression(self, p):
        return("compare", "greaterequal", p.expression0, p.expression1, p)

    @_("L_BRACE expression LESS_THAN ASSIGN expression  R_BRACE")
    def expression(self, p):
        return("compare", "lesserequal", p.expression0, p.expression1, p)

    @_('"-" expression %prec UMINUS')
    def expression(self, p):
        return -p.expression

    @_("IMPORT STRING")
    def expression(self, p):
        return ("import", p.STRING)


    def error(self, p):
        if type(p) == Token:
            line_number = p.line_number
            line = self.raw_prog.split("\n")[line_number-1]
        
            error_message(p, line, "Parser", message="Syntax error")
        else:
            print("reached end of file. Are you missing a semi colon ?")

        return None




    

    

    


    

    
    


    