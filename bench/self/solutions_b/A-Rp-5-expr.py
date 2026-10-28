import fractions
import re

def evaluate(s: str) -> fractions.Fraction:
    tokens = re.findall(r'\d+|[+*/\-()]|\*\*', s.replace(' ', ''))
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
        return parse_addition()

    def parse_addition():
        node = parse_multiplication()
        while peek() in ('+', '-'):
            op = consume()
            right = parse_multiplication()
            if op == '+':
                node += right
            else:
                node -= right
        return node

    def parse_multiplication():
        node = parse_unary()
        while peek() in ('*', '/'):
            op = consume()
            right = parse_unary()
            if op == '*':
                node *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                node /= right
        return node

    def parse_unary():
        if peek() in ('+', '-'):
            op = consume()
            node = parse_exponent()
            if op == '+':
                return node
            else:
                return -node
        return parse_exponent()

    def parse_exponent():
        node = parse_primary()
        if peek() == '**':
            consume()
            # Exponentiation is right-associative
            exponent = parse_exponent()
            if exponent.denominator != 1:
                raise ValueError("Exponent must be an integer")
            exp_val = int(exponent.numerator)
            # Handle 0**0 or negative exponents via standard Fraction/pow rules
            # but spec says raise ValueError if exponent is not integer.
            # 2**-1 is allowed if the exponent evaluates to -1.
            try:
                return node ** exp_val
            except ZeroDivisionError:
                raise ZeroDivisionError("division by zero")
        return node

    def parse_primary():
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
        raise ValueError("Trailing tokens")
    return result
