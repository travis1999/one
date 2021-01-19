from string import digits, ascii_letters
from random import choice

def unique_id(length = 8):
    letters = ""
    for _ in range(length):
        let = choice(choice([digits, ascii_letters]))
        letters += let


    return letters


class Execute: 
    def __init__(self): 
        self.env = {}
        self.funcs = {}
        self.stacks = {}
        

    def execute(self, tree):
        self.env = {}
        self.funcs = {}
        self.stacks = {"global": {}}
        self.stack_name = "global"
        self.returned = None

        print("________________")
        print(tree)
        print("_________________")

        result = None

        # try:
        result = self.walkTree(tree)
        
        
        # except Exception as e:
        #     print(e)
        #     print(tree)
        #     print(self.env)
        #     print(self.funcs)
        #     print(self.stacks)

        print(tree)
        print(self.env)
        print(self.funcs)
        print(self.stacks)


        if result is not None and isinstance(result, int): 
            return result
        if isinstance(result, str) and result[0] == '"': 
            return result
  
    def walkTree(self, node): 
        print("<node>")
        print(node)
        print("</node>")
        if isinstance(node, int): 
            return node 
            
        if isinstance(node, str): 
            return node 

        if node is None: 
            return None

        if node[0] == 'program':
            if node[1] == None: 
                self.walkTree(node[2]) 
            else: 
                self.walkTree(node[1]) 
                self.walkTree(node[2]) 

        if node[0] == 'func_call':
            self.returned = None
            if node[1] == "print":
                result = [self.walkTree(x) for x in node[2]]
                print(*result)

            else:
                name = node[1]
                stack_name = unique_id()
                self.stack_name = stack_name
                self.stacks[stack_name] = {}
                if name in self.funcs:
                    func_vars = self.funcs[name][0]
                    prog = self.funcs[name][1]

                    if len(func_vars) == len(node[2]):
                        
                        for _name, var in zip(func_vars, node[2]):
                            self.stacks[stack_name].update({_name: var})

                        print("*"*10)
                        print(prog)
                        print("*"*10)
                        result = self.walkTree(prog)
                        self.stack_name = "global"

                    else:
                        print(f"{len(func_vars)} arguments required found {len(node[2])}")
                else:
                    print(f"unknown function '{name}' ")

                if self.returned:
                    return self.returned
                



        if node[0] == 'var':
            if node[1] == "c_in":
                print('ok')
            if node[1] in self.stacks[self.stack_name]:
                return self.stacks[self.stack_name][node[1]]
            else:
                print(f"Unknown variable {node[1]}")

        if node[0] == "expr":
            return self.walkTree(node[1])

        if node[0] == "arithmetic":
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

        if node[0] == "var_decl_dynamic":
            self.stacks[self.stack_name][node[1]] = self.walkTree(node[2])

        if node[0] == "func_def_void":
            self.funcs[node[1]] = [None, node[2]]

        if node[0] == "func_def_args":
            self.funcs[node[1]] = [node[2], node[3]]

        if node[0] == "return_stack":
            temp = self.walkTree(node[1])
            # print(node, self.stack_name,  temp, "<-")
            self.returned = temp
            return temp
            
            



        
