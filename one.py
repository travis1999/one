from lexer import Tokenizer
from oneparser import OneParser
from execute import Execute


def main():
    print("one version 0.0.1a on python 3.8 64 bit")

    lines = []
    tokenizer = Tokenizer()
    parser = OneParser()
    executer = Execute()

    while True:
        print()
        line = input(">>> ")

        try:
            if line == "prog":
                for line in lines:
                    print(line)
            elif line in ["quit", "end"]:
                quit()

            elif line == "test":
                with open("test.ne", "r") as code:
                    cont = code.read()
                    res, content = tokenizer.tokenize(cont)

                    if res:
                        # for y in content:
                        #     print(y)
                        parser.raw_prog = tokenizer.raw_program
                        result = parser.parse((x for x in content))
                        if result:
                            evaluation = executer.execute(result)
                            
                    else:
                        print("Failed to execute last line")


            else:
                res, content = tokenizer.tokenize(line)
                if res:
                    for y in content:
                        print(y)
                    parser.raw_prog = tokenizer.raw_program
    
                    result = parser.parse((x for x in content))
                   

                else:
                    print("Failed to execute last line")

        except KeyboardInterrupt:
            print("Quiting")
            exit(0)

        

if __name__ == "__main__":
    main()