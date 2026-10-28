import fractions
import re

_TOKEN_RE = re.compile(r"\s*(?:(\d+)|(\*\*|[+\-*/()]))")


def _tokenize(s):
    tokens = []
    pos = 0
    s_stripped = s.rstrip()
    while pos < len(s_stripped):
        m = _TOKEN_RE.match(s_stripped, pos)
        if not m:
            raise ValueError("unexpected character in input")
        if m.group(1) is not None:
            tokens.append(("NUM", int(m.group(1))))
        else:
            tokens.append(("OP", m.group(2)))
        pos = m.end()
    tokens.append(("END", None))
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i]

    def advance(self):
        tok = self.tokens[self.i]
        self.i += 1
        return tok

    def expect_op(self, op):
        tok = self.advance()
        if tok != ("OP", op):
            raise ValueError("syntax error")

    def parse_expression(self):
        value = self.parse_term()
        while self.peek() in (("OP", "+"), ("OP", "-")):
            op = self.advance()[1]
            rhs = self.parse_term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def parse_term(self):
        value = self.parse_unary()
        while self.peek() in (("OP", "*"), ("OP", "/")):
            op = self.advance()[1]
            rhs = self.parse_unary()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ValueError("division by zero")
                value = value / rhs
        return value

    def parse_unary(self):
        if self.peek() == ("OP", "-"):
            self.advance()
            return -self.parse_unary()
        if self.peek() == ("OP", "+"):
            self.advance()
            return self.parse_unary()
        return self.parse_power()

    def parse_power(self):
        base = self.parse_atom()
        if self.peek() == ("OP", "**"):
            self.advance()
            exp = self.parse_unary()
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exp)
            if base == 0 and e < 0:
                raise ValueError("zero cannot be raised to a negative power")
            return base ** e
        return base

    def parse_atom(self):
        tok = self.advance()
        if tok[0] == "NUM":
            return fractions.Fraction(tok[1])
        if tok == ("OP", "("):
            value = self.parse_expression()
            self.expect_op(")")
            return value
        raise ValueError("syntax error")


def evaluate(s: str) -> fractions.Fraction:
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    tokens = _tokenize(s)
    parser = _Parser(tokens)
    result = parser.parse_expression()
    if parser.peek() != ("END", None):
        raise ValueError("syntax error")
    return fractions.Fraction(result)
