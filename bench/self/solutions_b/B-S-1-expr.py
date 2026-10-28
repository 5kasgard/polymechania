import fractions
import re

def evaluate(s: str) -> fractions.Fraction:
    # Tokenizer
    tokens = []
    # Regex for numbers, operators, and parentheses
    # Order matters: ** must be matched before *
    token_pattern = re.compile(r'\d+|(?:\*\*)|(?:\*)|(?:\+)|(?:\-)|(?:\/)|(?:\()|(?:\))')
    
    # We need to handle whitespace by ignoring it, but the regex handles it by not matching it.
    # However, we must ensure we don't skip invalid characters.
    # Let's use a more robust approach.
    
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        
        # Check for multi-char operators first
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
            tokens.append(fractions.Fraction(int(s[start:i])))
        else:
            raise ValueError(f"Invalid character: {s[i]}")

    pos = 0

    def parse_expression():
        nonlocal pos
        # Addition and Subtraction (lowest precedence, left-associative)
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
        # Multiplication and Division (left-associative)
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
        # Unary + and -
        if pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos += 1
            node = parse_unary() # Right associative/recursive for unary
            if op == '+':
                return node
            else:
                return -node
        return parse_exponent()

    def parse_exponent():
        nonlocal pos
        # Exponentiation (highest precedence, right-associative)
        # Note: -2**2 is (-2)**2 or -(2**2)? 
        # Spec says: "Note -2**2 == -4". This implies ** is higher than unary minus.
        # But spec also says: "Precedence: ** highest ... then unary +/-, then * and /".
        # If ** is highest, then -2**2 is -(2**2) = -4. Correct.
        # If unary is higher, then (-2)**2 = 4.
        # The spec says: "** highest ... then unary". So 2**3**2 is 2**(3**2).
        
        node = parse_primary()
        if pos < len(tokens) and tokens[pos] == '**':
            pos += 1
            exponent_node = parse_exponent() # Right associative
            
            # Exponents must be integers
            if exponent_node.denominator != 1:
                raise ValueError("Exponent must be an integer")
            
            exp_val = exponent_node.numerator
            try:
                # Use pow for large integers, but handle negative exponents
                if exp_val < 0:
                    node = fractions.Fraction(1, pow(node.denominator, -exp_val) * pow(node.numerator, -exp_val))
                    # Wait, the above is wrong for fractions. 
                    # (a/b)^-n = (b/a)^n
                    base = node
                    node = (1 / base) ** abs(exp_val)
                else:
                    # node is a Fraction. (a/b)^n = a^n / b^n
                    node = node ** exp_val
            except ZeroDivisionError:
                raise ZeroDivisionError("division by zero")
            except OverflowError:
                # In case of extremely large numbers, though Python handles large ints
                raise ValueError("Result too large")
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
        elif isinstance(token, fractions.Fraction):
            pos += 1
            return token
        else:
            raise ValueError(f"Unexpected token: {token}")

    result = parse_expression()
    
    if pos < len(tokens):
        raise ValueError("Unexpected extra tokens")
        
    return result
