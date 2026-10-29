import fractions
import re


_TOKEN_RE = re.compile(r"\s*(?:(\d+)|(\*\*|[-+*/()]))")


def _tokenize(s):
    tokens = []
    pos = 0
    s = s.rstrip()
    while pos < len(s):
        m = _TOKEN_RE.match(s, pos)
        if not m or m.end() == pos:
            if s[pos:].strip() == "":
                break
            raise ValueError("invalid syntax")
        if m.group(1) is not None:
            tokens.append(("num", int(m.group(1))))
        else:
            tokens.append(("op", m.group(2)))
        pos = m.end()
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def advance(self):
        tok = self.peek()
        if tok is None:
            raise ValueError("unexpected end of input")
        self.i += 1
        return tok

    def is_op(self, tok, value):
        return tok is not None and tok[0] == "op" and tok[1] == value

    def parse(self):
        if not self.tokens:
            raise ValueError("empty expression")
        value = self.parse_expr()
        if self.peek() is not None:
            raise ValueError("unexpected token")
        return value

    def parse_expr(self):
        value = self.parse_term()
        while True:
            tok = self.peek()
            if self.is_op(tok, "+"):
                self.advance()
                value = value + self.parse_term()
            elif self.is_op(tok, "-"):
                self.advance()
                value = value - self.parse_term()
            else:
                return value

    def parse_term(self):
        value = self.parse_unary()
        while True:
            tok = self.peek()
            if self.is_op(tok, "*"):
                self.advance()
                value = value * self.parse_unary()
            elif self.is_op(tok, "/"):
                self.advance()
                divisor = self.parse_unary()
                if divisor == 0:
                    raise ValueError("division by zero")
                value = value / divisor
            else:
                return value

    def parse_unary(self):
        tok = self.peek()
        if self.is_op(tok, "-"):
            self.advance()
            return -self.parse_unary()
        if self.is_op(tok, "+"):
            self.advance()
            return self.parse_unary()
        return self.parse_power()

    def parse_power(self):
        base = self.parse_atom()
        if self.is_op(self.peek(), "**"):
            self.advance()
            exponent = self.parse_unary()
            if exponent.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exponent)
            if base == 0 and e < 0:
                raise ValueError("division by zero")
            return base ** e
        return base

    def parse_atom(self):
        tok = self.advance()
        if tok[0] == "num":
            return fractions.Fraction(tok[1])
        if tok[1] == "(":
            value = self.parse_expr()
            closing = self.advance()
            if not self.is_op(closing, ")"):
                raise ValueError("expected ')'")
            return value
        raise ValueError("unexpected token")


def evaluate(s: str) -> fractions.Fraction:
    tokens = _tokenize(s)
    result = _Parser(tokens).parse()
    return fractions.Fraction(result)
