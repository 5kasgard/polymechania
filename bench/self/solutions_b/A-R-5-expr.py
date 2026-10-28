import fractions
import re

def evaluate(s: str) -> fractions.Fraction:
    """
    Evaluates an arithmetic expression with exact rational results.
    Supports +, -, *, /, **, unary +/-, and parentheses.
    """
    tokens = re.findall(r'\d+|[+*/\-()]|\*\*', s)
    
    # Check for invalid characters by comparing reconstructed string length
    # (ignoring whitespace)
    if len("".join(tokens)) != len(re.sub(r'\s+', '', s)):
        # This is a simple check; a more robust one would check if tokens 
        # cover all non-whitespace characters.
        pass 

    # Re-verify tokens against original string to catch illegal characters
    clean_s = re.sub(r'\s+', '', s)
    token_str = "".join(tokens)
    if len(token_str) != len(clean_s):
        raise ValueError("Syntax error")

    pos = 0

    def parse_expression() -> fractions.Fraction:
        nonlocal pos
        node = parse_term()
        while pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos += 1
            right = parse_term()
            if op == '+':
                node += right
            else:
                node -= right
        return node

    def parse_term() -> fractions.Fraction:
        nonlocal pos
        node = parse_unary()
        while pos < len(tokens) and tokens[pos] in ('*', '/'):
            op = tokens[pos]
            pos += 1
            right = parse_unary()
            if op == '*':
                node *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                node /= right
        return node

    def parse_unary() -> fractions.Fraction:
        nonlocal pos
        if pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos += 1
            node = parse_unary()
            if op == '+':
                return node
            else:
                return -node
        return parse_exponent()

    def parse_exponent() -> fractions.Fraction:
        nonlocal pos
        node = parse_primary()
        if pos < len(tokens) and tokens[pos] == '**':
            pos += 1
            # Exponentiation is right-associative
            right = parse_exponent()
            # Exponent must be an integer
            if right.denominator != 1:
                raise ValueError("Exponent must be an integer")
            exponent = right.numerator
            try:
                # Use pow for integer exponentiation with Fraction
                return fractions.Fraction(node ** exponent)
            except ZeroDivisionError:
                raise ZeroDivisionError("division by zero")
            except OverflowError:
                # Handle extremely large results if necessary, 
                # though Fraction handles arbitrary size
                raise
        return node

    def parse_primary() -> fractions.Fraction:
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError("Unexpected end of input")
        
        token = tokens[pos]
        if token == '(':
            pos += 1
            node = parse_expression()
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("Missing closing parenthesis")
            pos += 1
            return node
        elif token == ')':
            raise ValueError("Unexpected closing parenthesis")
        elif token.isdigit():
            pos += 1
            return fractions.Fraction(int(token))
        elif token == '-': # Handle case where unary might be missed by precedence
             raise ValueError("Unexpected minus")
        elif token == '+':
             raise ValueError("Unexpected plus")
        else:
            raise ValueError(f"Unexpected token: {token}")

    try:
        result = parse_expression()
        if pos < len(tokens):
            raise ValueError("Trailing tokens")
        return result
    except (IndexError, ValueError) as e:
        if isinstance(e, ZeroDivisionError):
            raise e
        raise ValueError("Syntax error") from e

