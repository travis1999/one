from string import ascii_letters, digits
import string
from typing import Any, List
from utils import error_message

class Token:
    def __init__(self, TYPE: str, value: Any, line: int, start: int, end: int) -> None:
        self.type = TYPE
        self.value = value
        self.line_number = line
        self.start = start
        self.end = end


    def __str__(self) -> str:
        return f"TOKEN({self.type}, '{self.value}')"


class Tokenizer:
    tok = {
        "STRING", "ADD", "SUB", "MULT", "DIV", "MOD","TO",
        "ASSIGN", "L_BRACE", "R_BRACE", "L_SQBRACE",  "R_SQBRACE",
        "GREAT_THAN","LESS_THAN", "COLON", "COMMA", "DECLARATION",
        "FOR", "WHILE", "FUNC_DEF", "IF", "ELSE",  "BLOCK_START", "BLOCK_END",
        "RETURN", "NOT", "OR", "AND", "INT", "FLOAT", "IDENTIFIER", "SEMI"
        }

    def __init__(self) -> None:
        self.tokens = {"NUMBER": digits,
                       "STRING": ascii_letters,
                       "ADD": "+",
                       "SUB": "-",
                       "MULT": "*",
                       "DIV": "/",
                       "MOD": "%",
                       "ASSIGN": "=",
                       "L_BRACE": "(",
                       "R_BRACE": ")",
                       "L_SQBRACE": "[",
                       "R_SQBRACE": "]",
                       "GREAT_THAN": ">",
                       "LESS_THAN": "<",
                       "COLON": ":",
                       "COMMA": ",",
                       "DECLARATION": "var",
                       "FOR": "for",
                       "WHILE": "while",
                       "FUNC_DEF": "func",
                       "IF":"if", 
                       "ELSE":"else",  
                       "BLOCK_START":"do", 
                       "BLOCK_END":"end",
                       "RETURN":"return",
                       "NOT": "!",
                       "OR": "|",
                       "AND": "&",
                       "TO": "to",
                       "SEMI": ";"
                       }

        self.tokenized = []
        self.program = None
        self.current = None
        self.prog = None
        self.cont = True
        self.raw_program = None

    def new_session(self, program: str) -> None:
        self.tokenized = []
        self.program = None
        self.current_line = None
        self.program = (x for x in program.split("\n"))
        self.prog = self.generate()
    
    def generate(self):
        line_no = 1
        position = 1
        for line in self.program:
            self.current_line = line
            for char in line:
                yield [char, line_no, position]
                position += 1
            line_no += 1
            position = 1

        
    def advance(self):
        try:

            return next(self.prog)
        except StopIteration:
            return None, None, None

    def make_number(self, digit):
        pass

    def get_key(self, val):
        for key, value in self.tokens.items():
            if val == value:
                return key

    def make_string(self, char: tuple):
        temp: str = ""+char[0]

        start = char[2]
        end = int(char[2])
        line = char[1]
        next_char = None
        scan = True

        is_string = True if char[0] == '"' else False
        while scan:
            next_char = self.advance()

            if next_char[0] == None:
                break

            if next_char[0] in list(self.tokens.values())[3:] and not is_string:
                self.cont = False
                break

            if next_char[0] == " ":
                if not is_string:
                    break

            if next_char[0] == '"' and is_string:
                scan = False


            if next_char[0] not in string.ascii_letters+string.digits+"_":
                if not is_string:
                    # error_message(Token("IDENTIFIER", temp+char[0], char[1], start, end+1), self.current_line, "Tokenizer",
                    # message=f"Character '{next_char[0]}' not allowed in identifier")
                    # return False, None
                    self.cont = False
                    break

            end = next_char[2]
            temp += next_char[0]


        if is_string and not temp.endswith('"'):
            error_message(Token("STRING", temp+char[0], char[1], start, end+1), self.current_line, "Tokenizer",
                    message=f"Character '\"' Expected at the end of the string")
            return False, None
            
        if temp in list(self.tokens.values())[2:]:
            return next_char, Token(self.get_key(temp), temp, line, start, end)

        elif temp.startswith('"') and temp.endswith('"'):
            return next_char, Token("STRING", temp, line, start, end)

        else:
            return next_char, Token("IDENTIFIER", temp, line, start, end)

    def make_number(self, char) -> int:
        dot_count = 0
        num = char[0]

        start = char[2]
        end = int(char[2])
        line = char[1]

        if num[0] == ".":
            dot_count += 1

        while True:
            next_char = self.advance()
            if next_char[0] == None:
                break

            if next_char[0] in string.digits+".":
                num += next_char[0]
                end = next_char[2]
                if next_char[0] == ".":
                    dot_count += 1

            else:
                self.cont = False
                break


            if next_char[0] == ".":
                if dot_count > 1:
                    error_message(Token("NUMBER", num+char[0], char[1], start, end+2), self.current_line, "Tokenizer",
                    message=f"float has more than one '.' ")
                    return False, None
                
        if dot_count == 1:
             return next_char, Token("FLOAT", float(num), line, start, end)
        else:
             return next_char, Token("INT", int(num), line, start, end)





    def tokenize(self, program: str) -> List[Token]:
        self.raw_program = program
        self.new_session(program)
        

        char = None
        while True:
            if self.cont:
                char = self.advance()
            else:
                self.cont = True

            if char[0] == None:
                break

            if char[0] == " ":
                continue

            if char[0] in self.tokens["NUMBER"]+".":
                char, tok = self.make_number(char)
                if char == False:
                    return char, tok
                self.tokenized.append(tok)

            elif char[0] in self.tokens["STRING"] + '"':
                char, tok = self.make_string(char)
                if char == False:
                    return char, tok
                self.tokenized.append(tok)

            else:
                found = False
                last_token = None
                for token, value in self.tokens.items():
                    if value == char[0]:
                        self.tokenized.append(Token(token, *char, char[2]))
                        found = True
                        break
                    last_token = token

                if not found:
                    error_message(Token(last_token, *char, char[2]), self.current_line, unit="Tokenizer", message=f"Unknown token '{char[0]}'")
                    return False, None

        return True, self.tokenized

test_prog = """
func main args:
    do
        const var PI = 3.14
        var radius = 7
        var area = PI*radius*radius
        print("area is:"+area)
    end
"""


if __name__ == "__main__":

    tokenizer = Tokenizer()
    _, res = tokenizer.tokenize(test_prog)
    for x in res:
        print(x)





