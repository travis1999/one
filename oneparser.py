from lexer import Tokenizer
from sly import Parser
from utils import error_message

class OneParser(Parser):
    tokens = Tokenizer.tok

    debugfile = 'parser.out'
    
    precedence = (('left', ADD, SUB),
                  ('left', MULT, DIV),
                  ('right', 'UMINUS'),
                  ('left', BLOCK_START, BLOCK_END)
    )

    def __init__(self):
        self.env = {}
        self.scope = "global"
        self.raw_prog = None

    @_("statement")
    def program(self, p):
        return ("program", None, p.statement)

    @_("statement SEMI")
    def program(self, p):
        return ("program", None, p.statement)

    @_("statement SEMI program")
    def program(self, p):
        return("program", p.statement, p.program)


    @_("FUNC_DEF IDENTIFIER COLON BLOCK_START program BLOCK_END")
    def statement(self, p):
        return("func_def_void", p.IDENTIFIER, p.program)

    @_("FUNC_DEF IDENTIFIER f_args COLON program BLOCK_END")
    def statement(self, p):
        return("func_def_args", p.IDENTIFIER, p.f_args, p.program)

    @_("IF L_BRACE expression R_BRACE BLOCK_START program BLOCK_END")
    def statement(self, p):
        return ("if_setup", p.expression, p.program)

    @_("IF L_BRACE expression R_BRACE BLOCK_START program BLOCK_END ELSE BLOCK_START program BLOCK_END")
    def statement(self, p):
        return ("if_else_setup", p.expression, p.program0, p.program1)

    @_("WHILE L_BRACE expression R_BRACE BLOCK_START program BLOCK_END")
    def statement(self, p):
        return ("while_setup", p.expression, p.program)

    @_('FOR expression TO expression BLOCK_START program BLOCK_END')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.expression0, p.expression1), p.program)

    @_("RETURN expression")
    def statement(self, p):
        return ("return_stack", p.expression)

    @_("IDENTIFIER L_BRACE elements R_BRACE")
    def expression(self, p):
        return ("func_call", p.IDENTIFIER, p.elements)


    @_("DECLARATION IDENTIFIER ASSIGN statement")
    def statement(self, p):
        return ("var_decl_dynamic", p.IDENTIFIER, p.statement)

    @_("IDENTIFIER ASSIGN expression")
    def statement(self, p):
        return ("var_re_assign", p.IDENTIFIER, p.expression)

    @_("DECLARATION IDENTIFIER L_SQBRACE R_SQBRACE ASSIGN L_SQBRACE elements R_SQBRACE")
    def statement(self, p):
        return ("array_decl", p.identifier)

    @_("expression")
    def statement(self, p):
        return p.expression


    @_("DECLARATION IDENTIFIER")
    def f_args(self, p):
        return [p.IDENTIFIER]

    @_('f_args COMMA DECLARATION IDENTIFIER')
    def f_args(self, p):
        p.f_args.append(p.IDENTIFIER)
        return p.f_args

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
    def expression(self, p):
        return ("var", p.IDENTIFIER)

    @_("L_BRACE expression R_BRACE")
    def expression(self, p):
        return p.expression

    @_("IDENTIFIER L_SQBRACE expression R_SQBRACE")
    def expression(self, p):
        return ("element_access", p.IDENTIFIER, p.expression)

    @_("expression ADD expression")
    def expression(self, p):
        return("arithmetic", "add", p.expression0, p.expression1)

    @_("expression MOD expression")
    def expression(self, p):
        return("arithmetic", "mod", p.expression0, p.expression1)

    @_("expression SUB expression")
    def expression(self, p):
        return("arithmetic", "minus", p.expression0, p.expression1)

    @_("expression DIV expression")
    def expression(self, p):
        return("arithmetic", "div", p.expression0, p.expression1)

    @_("expression MULT expression")
    def expression(self, p):
        return("arithmetic", "mult", p.expression0, p.expression1)

    @_("expression NOT expression")
    def expression(self, p):
        return("compare", "not", p.expression0, p.expression1)

    @_("expression OR expression")
    def expression(self, p):
        return("compare", "or", p.expression0, p.expression1)

    @_("expression AND expression")
    def expression(self, p):
        return("compare", "and", p.expression0, p.expression1)

    @_("expression GREAT_THAN expression")
    def expression(self, p):
        return("compare", "greater", p.expression0, p.expression1)

    @_("expression LESS_THAN expression")
    def expression(self, p):
        return("compare", "lesser", p.expression0, p.expression1)

    @_("expression ASSIGN ASSIGN expression")
    def expression(self, p):
        return("compare", "equal", p.expression0, p.expression1)

    @_("expression NOT ASSIGN expression")
    def expression(self, p):
        return("compare", "notequal", p.expression0, p.expression1)

    @_("expression GREAT_THAN ASSIGN expression")
    def expression(self, p):
        return("compare", "greaterequal", p.expression0, p.expression1)

    @_("expression LESS_THAN ASSIGN expression")
    def expression(self, p):
        return("compare", "lesserequal", p.expression0, p.expression1)

    @_('"-" expression %prec UMINUS')
    def expression(self, p):
        return -p.expression

    def error(self, p):
        if p:
            line_number = p.line_number
            line = self.raw_prog.split("\n")[line_number-1]
            error_message(p, line, "Parser", message="Syntax error")
            print(p)
        else:
            print("reached end of file. Are you missing a semi colon ?")



    

    

    


    

    
    


    