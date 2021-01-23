from oneparser import OneParser
from lexer import Tokenizer, Token
from string import digits, ascii_letters
from random import choice
from utils import error_message


one_builtins = ["map", "string", "io"]


class Struct:
    def __init__(self, keys, values) -> None:
        self.struct = {}

        for key, value in zip(keys, values):
            self.struct.update({key: value})

    def __str__(self):
        return f"Struct {self.struct}"
        

    def reassign(self, key, value):
        self.struct[key] = value

    def access(self, key):
        return self.struct[key]



class Execute: 
    def __init__(self): 
        self.env = {}
        self.funcs = {}
        self.structs = {}
        self.globals = {"true": True, "false": False, "none": None}
        self.stacks = {"global": {}}
        self.stack_name = "global"
        self.stop = False
        self.returned = None
        self.prog = None
        

    def execute(self, tree, prog, clear_env: bool):
        self.prog = prog
        if clear_env:
            self.env = {}
            self.funcs = {}
            self.stacks = {"global": {}}
            self.stack_name = "global"
            self.returned = None
        # try:
        result = self.walkTree(tree)
        return result

    def exec_err(self, token, message):
            print(token._slice)
            print(token._namemap)
            print(token._stack)
            print(token.lineno)
            print(token.index)

            tok = None
            for x in token._slice:
                if isinstance(x, Token):
                    tok = x
                    print(tok.type)
                
            if tok:
                line_number = tok.line_number
                print(self.prog.split("\n") , line_number)
                line = self.prog.split("\n")[line_number-1]
                tok.start = 0
                tok.end = len(line)
                error_message(tok, line, "Executor", message=message)
            else:
                print(message)


    @staticmethod
    def unique_id(length = 8):
        letters = ""
        for _ in range(length):
            let = choice(choice([digits, ascii_letters]))
            letters += let
        return letters

    def one_import(self, module: str) -> None:
        file = None
        if module in one_builtins:
            file = f"builtins/{module}.ne"
        else:
            file = module+".ne"


        with open(file, "r") as code:
            source = code.read()
            tokenizer = Tokenizer()
            parser = OneParser()
            executer = Execute()

            success, tokens = tokenizer.tokenize(source)
            if success:
                parser.raw_prog = tokenizer.raw_program
                result = parser.parse((x for x in tokens))
                if result:
                    evaluation = executer.execute(result, True)
                    mod_vars = executer.stacks["global"]
                    mod_funcs = executer.funcs

                    self.stacks["global"].update(mod_vars)
                    self.funcs.update(mod_funcs)
                   
  
    def walkTree(self, node): 
        # print()
        # print("<n>")
        # print(node)
        # print("<n>")
        # print()

        if self.returned:
            return None


        if isinstance(node, int): 
            return node 
            
        if isinstance(node, str): 
            return node[1:-1]

        if isinstance(node, list): 
            return node 

        if isinstance(node, float): 
            return node 

        
        if node is None: 
            return None

        if node[0] == 'program':
            if node[1] == None: 
                self.walkTree(node[2]) 
            else: 
                self.walkTree(node[2]) 
                self.walkTree(node[1]) 

        elif node[0] == 'func_call':
            self.returned = None
            if node[1] == "print":
                result = [self.walkTree(x) for x in node[2]]

                for idx, res in enumerate(result):
                    if type(res) == str:
                        result[idx] = res.strip('"')
                        
                print(*result)

            elif node[1] == "len":
                result = self.walkTree(node[2][0]) 
                return len(result)

            elif node[1] == "py_call":
                result = [self.walkTree(x) for x in node[2][1:]]
                function = __builtins__[node[2][0].strip('"')]

                return function(*result)


            else:
                name = node[1]
                stack_name = self.unique_id()
                self.stack_name = stack_name
                self.stacks[stack_name] = {}
                if name in self.funcs:
                    func_vars = self.funcs[name][0]
                    prog = self.funcs[name][1]

                    if len(func_vars) == len(node[2]):

                        simplified = [self.walkTree(x) for x in node[2]]
                        for _name, var in zip(func_vars, simplified):
                            self.stacks[stack_name].update({_name: var})

                        result = self.walkTree(prog)
                        self.stack_name = "global"

                    else:
                        print(f"{len(func_vars)} arguments required found {len(node[2])}")
                else:
                    print(f"unknown function '{name}' ")

                if self.returned:
                    temp = self.returned
                    self.returned = None
                    return temp
                

        elif node[0] == 'var':
            if node[1] in self.stacks[self.stack_name]:
                return self.stacks[self.stack_name][node[1]]

            else:
                if node[1] in self.stacks["global"]:
                    return self.stacks["global"][node[1]]
                
                else:
                    self.exec_err(node[-1], f"Variable {node[1]} not defined")

        elif node[0] == "expr":
            return self.walkTree(node[1])

        elif node[0] == "arithmetic":
            if node[1] == "add":
                return self.walkTree(node[2]) + self.walkTree(node[3])
            if node[1] == "mult":
                return self.walkTree(node[2]) * self.walkTree(node[3])
            if node[1] == "div":
                return self.walkTree(node[2]) / self.walkTree(node[3])
            if node[1] == "minus":
                return self.walkTree(node[2]) - self.walkTree(node[3])
            if node[1] == "mod":
                return self.walkTree(node[2]) % self.walkTree(node[3])

        elif node[0] == "var_decl_dynamic":
            self.stacks[self.stack_name][node[1]] = self.walkTree(node[2])

        elif node[0] == "var_re_assign":
            if node[1] in self.stacks[self.stack_name]:
                self.stacks[self.stack_name][node[1]] = self.walkTree(node[2])
                
            else:
                self.exec_err(node[-1], f"Variable {node[1]} not defined")

        elif node[0] == "func_def_void":
            self.funcs[node[1]] = [[], node[2]]

        elif node[0] == "func_def_args":
            self.funcs[node[1]] = [node[2], node[3]]

        elif node[0] == "return_stack":
            temp = self.walkTree(node[1])
            # print(node, self.stack_name,  temp, "<-")
            self.returned = temp

            return temp

        #############################
        # COMPARISON
        #############################

        elif node[0] == "compare":
            if node[1] == "or":
                return (self.walkTree(node[2]) or self.walkTree(node[3]))

            elif node[1] == "and":
                return (self.walkTree(node[2]) and self.walkTree(node[3]))

            elif node[1] == "greater":
                return (self.walkTree(node[2]) > self.walkTree(node[3]))

            elif node[1] == "lesser":
                return (self.walkTree(node[2]) < self.walkTree(node[3]))

            elif node[1] == "equal":
                return (self.walkTree(node[2]) == self.walkTree(node[3]))

            elif node[1] == "notequal":
                return (self.walkTree(node[2]) != self.walkTree(node[3]))

            elif node[1] == "greaterequal":
                return (self.walkTree(node[2]) >= self.walkTree(node[3]))

            elif node[1] == "lesserequal":
                return (self.walkTree(node[2]) <= self.walkTree(node[3]))

            
        #############################
        # while loop
        #############################
        elif node[0] == "while_setup":
            while self.walkTree(node[1]):
                self.walkTree(node[2])


        #############################
        # for loop
        #############################
        elif node[0] == "for_loop":
            new_var = False
            if not node[1] in self.stacks[self.stack_name]:
                self.stacks[self.stack_name][node[1]] = 0
                new_var = True

            for x in self.walkTree(node[2]):
                self.stacks[self.stack_name][node[1]] = x
                self.walkTree(node[3])

            if new_var:
                del self.stacks[self.stack_name][node[1]]

        #############################
        # if statement
        #############################
        if node[0] == "if_statement":
            if self.walkTree(node[1]):
                self.walkTree(node[2])

        #############################
        # if else statement
        #############################
        if node[0] == "if_else_statement":
            if self.walkTree(node[1]):
                self.walkTree(node[2])
            else:
                self.walkTree(node[3])


        #############################
        # arrays
        #############################
    

        elif node[0] ==  "array_decl":
            temp = self.walkTree(node[2])
            new = [self.walkTree(x) for x in temp]
            self.stacks[self.stack_name][node[1]] = new

        elif node[0] == "array_re_assign":
            if node[1] in self.stacks[self.stack_name]:
                temp = self.walkTree(node[2])
                new = [self.walkTree(x) for x in temp]
                self.stacks[self.stack_name][node[1]] = new
            else:
                print("Array was not defined")

        elif node[0] == "element_access":
            if node[1] in self.stacks[self.stack_name]:
                array = self.stacks[self.stack_name][node[1]] 
                index = self.walkTree(node[2])
                try:
                    element = array[index]
                    return element

                except IndexError:
                    print(f"integer required to access elements of array {array}")

            else:
                print(f"Array {node[1]} not defined")

        ######################
        # IMPORTS
        ######################

        elif node[0] == "import":
            self.one_import(node[1].strip('"'))


        #######################
        # STRUCTS
        #######################
        elif node[0] == "struct_def":
            self.structs.update({node[1]: node[2]})

        elif node[0] == "struct_assign":
            if node[1] in self.structs:
                walked = [self.walkTree(x) for x in node[2]]
                return Struct(self.structs[node[1]], walked)

        elif node[0] == "struct_element_access":

            if node[1] in self.stacks[self.stack_name]:
                obj = self.stacks[self.stack_name][node[1]]

                if isinstance(obj, Struct):
                    return obj.access(node[2])
            else:
                print("unknown element")

        elif node[0] == "struct_element_reassign":
            if node[1] in self.stacks[self.stack_name]:
                obj = self.stacks[self.stack_name][node[1]]

                walked = self.walkTree(node[3])
                if isinstance(obj, Struct):
                    return obj.reassign(node[2], walked)
            else:
                print("unknown element")








            
            



        
