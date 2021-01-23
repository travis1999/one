def error_message(token, line, unit, file=None, message="Not defined"):
    print(f"Error in execution({unit})")
    print(f"File '{file}', line {token.line_number}")
    
    length = token.end-token.start if token.end-token.start > 0 else 1
    error_mark = "^"*length
    line_f = f"{token.line_number}.| "
    
    print(f"{line_f}{line}")
    print(f"{' '*len(line_f)}{error_mark:>{token.start}}")
    print(f"Error: {message}\n")
    