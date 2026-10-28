import fractions
import re

def evaluate(s: str) -> fractions.Fraction:
    """
    Evaluates an arithmetic expression with exact rational results.
    Supports +, -, *, /, **, unary +/-, and parentheses.
    """
    # Tokenize the input string
    # Tokens: numbers (including decimals if needed, though spec says integers), 
    # operators, parentheses.
    tokens = re.findall(r'\d+|[+\-*/()]|\*\*', s)
    # Note: The regex above might split ** into * and *. 
    # Let's refine the tokenizer to handle ** correctly.
    tokens = []
    i = 0
    s_clean = s.replace(" ", "")
    while i < len(s_clean):
        if s_clean[i:i+2] == '**':
            tokens.append('**')
            i += 2
        elif s_clean[i] in '+-*/()':
            tokens.append(s_clean[i])
            i += 1
        elif s_clean[i].isdigit():
            j = i
            while j < len(s_clean) and s_clean[j].isdigit():
                j += 1
            tokens.append(s_clean[i:j])
            i = j
        else:
            raise ValueError(f"Unexpected character: {s_clean[i]}")

    pos = 0

    def peek():
        nonlocal pos
        return tokens[pos] if pos < len(tokens) else None

    def consume(expected=None):
        nonlocal pos
        token = peek()
        if expected and token != expected:
            raise ValueError(f"Expected {expected}, got {token}")
        pos += 1
        return token

    def parse_expression():
        # Addition and Subtraction (left-associative)
        node = parse_term()
        while peek() in ('+', '-'):
            op = consume()
            right = parse_term()
            if op == '+':
                node += right
            else:
                node -= right
        return node

    def parse_term():
        # Multiplication and Division (left-associative)
        node = parse_unary()
        while peek() in ('*', '/'):
            op = consume()
            right = parse_unary()
            if op == '*':
                node *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                node /= right
        return node

    def parse_unary():
        # Unary plus and minus
        if peek() == '+':
            consume()
            return parse_unary()
        if peek() == '-':
            consume()
            return -parse_unary()
        return parse_power()

    def parse_power():
        # Exponentiation (right-associative)
        node = parse_factor()
        if peek() == '**':
            consume()
            exponent_val = parse_power()
            # Spec: Exponents must be integers after evaluation
            if exponent_val.denominator != 1:
                raise ValueError("Exponent must be an integer")
            exponent = exponent_val.numerator
            # Use integer power for efficiency and to handle negative exponents correctly
            try:
                node = fractions.Fraction(pow(node.numerator, exponent), pow(node.denominator, exponent))
            except OverflowError:
                # For very large results, though Fraction handles arbitrary size
                raise ValueError("Result too large")
            # Note: pow(int, int) handles negative exponents by returning float, 
            # but we need Fraction. 
            # Correct way for Fraction ** int:
            if exponent >= 0:
                node = node ** exponent
            else:
                node = 1 / (node ** abs(exponent))
            return node
        return node

    def parse_factor():
        token = peek()
        if token == '(':
            consume('(')
            node = parse_expression()
            consume(')')
            return node
        elif token and token.isdigit():
            return fractions.Fraction(int(consume()))
        else:
            raise ValueError(f"Unexpected token: {token}")

    result = parse_expression()
    
    if pos < len(tokens):
        raise ValueError("Trailing tokens in expression")
        
    return result
