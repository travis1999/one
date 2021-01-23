from lexer import Tokenizer
from oneparser import OneParser
from execute import Execute


lines = []
tokenizer = Tokenizer()
parser = OneParser()
executer = Execute()


def evaluate(code: str, clear_env=True) -> str:
    res, content = tokenizer.tokenize(code)

    if res:
        parser.raw_prog = tokenizer.raw_program
        result = parser.parse((x for x in content))
        if result:
            evaluation = executer.execute(result, tokenizer.raw_program, clear_env)
            return evaluation
            
    else:
        print("Failed to execute last line")
        return False


def main() -> None:
    global lines
    print("one version 0.0.1a on python 3.9.1 64 bit")
    env = {}
    while True:
        print()
        line = input(">>> ")

        try:
            if line == ":prog":
                for line in lines:
                    print(line)
            elif line in [":quit", ":end"]:
                quit()

            elif line == ":run":
                while True:
                    file_name = input("Input file name: ")

                    if file_name == ":cancel":
                        break
                    try:
                        with open(file_name, "r") as code:
                            cont = code.read()
                            print()
                            evaluate(cont)
                            break
                    except FileNotFoundError:
                        print(f"File {file_name} not found.")

            else:
                evaluate(line, False)
           
        except KeyboardInterrupt:
            print("Quiting")
            exit(0)

        

if __name__ == "__main__":
    main()