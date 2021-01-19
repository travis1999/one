def error_message(token, line, unit, file=None, message="Not defined"):
    print(f"Error in execution({unit}) \n")
    print(f"File '{file}', line {token.line_number}")
    print(line)
    length = token.end-token.start if token.end-token.start > 0 else 1

    error_mark = "^"*length
    print(f"{error_mark:>{token.start}}")

    print(f"Error: {message}\n")