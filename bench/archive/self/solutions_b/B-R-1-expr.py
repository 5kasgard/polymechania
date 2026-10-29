import fractions
import re

def evaluate(s: str) -> fractions.Fraction:
    # Tokenize the input string
    tokens = []
    # Regex for numbers, operators, and parentheses
    # We use a simple scanner approach
    pattern = re.compile(r'\d+|[\+\-\*\/\(\)\*\*]')
    
    # Since ** is two characters, we need to handle it carefully.
    # Let's refine the tokenizer to handle multi-char operators.
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        if s[i:i+2] == '**':
            tokens.append('**')
            i += 2
        elif s[i] in '+-*/()':
            tokens.append(s[i])
            i += 1
        elif s[i].isdigit():
            start = i
            while i < len(s) and s[i].isdigit():
                i += 1
            tokens.append(s[start:i])
        else:
            raise ValueError("Invalid character")

    pos = 0

    def parse_expression():
        nonlocal pos
        # Level 1: + and - (left-associative)
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

    def parse_term():
        nonlocal pos
        # Level 2: * and / (left-associative)
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

    def parse_unary():
        nonlocal pos
        # Level 3: unary + and -
        if pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos += 1
            node = parse_exponent()
            if op == '+':
                return node
            else:
                return -node
        return parse_exponent()

    def parse_exponent():
        nonlocal pos
        # Level 4: ** (right-associative)
        node = parse_primary()
        if pos < len(tokens) and tokens[pos] == '**':
            pos += 1
            exponent_node = parse_exponent()
            # Exponent must be an integer
            if exponent_node.denominator != 1:
                raise ValueError("Exponent must be an integer")
            exp = exponent_node.numerator
            # Handle 0**0 or negative exponents for base 0
            if node == 0 and exp < 0:
                raise ZeroDivisionError("division by zero")
            # Python's ** behavior: 0**0 is 1
            node = fractions.Fraction(node ** exp)
            return node
        return node

    def parse_primary():
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
        elif token.isdigit():
            pos += 1
            return fractions.Fraction(int(token))
        else:
            raise ValueError(f"Unexpected token: {token}")

    try:
        result = parse_expression()
        if pos != len(tokens):
            raise ValueError("Trailing tokens")
        return result
    except (IndexError, TypeError):
        raise ValueError("Syntax error")

