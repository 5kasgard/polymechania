import fractions
import re


_TOKEN_RE = re.compile(r"\s*(?:(\d+)|(\*\*|[-+*/()]))")


def _tokenize(s):
    tokens = []
    pos = 0
    n = len(s)
    while pos < n:
        if s[pos:].strip() == "":
            break
        m = _TOKEN_RE.match(s, pos)
        if not m:
            raise ValueError("invalid syntax at position %d" % pos)
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
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return None

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
        value = self.expr()
        if self.peek() is not None:
            raise ValueError("unexpected token")
        return value

    def expr(self):
        value = self.term()
        while True:
            tok = self.peek()
            if self.is_op(tok, "+"):
                self.advance()
                value = value + self.term()
            elif self.is_op(tok, "-"):
                self.advance()
                value = value - self.term()
            else:
                return value

    def term(self):
        value = self.unary()
        while True:
            tok = self.peek()
            if self.is_op(tok, "*"):
                self.advance()
                value = value * self.unary()
            elif self.is_op(tok, "/"):
                self.advance()
                divisor = self.unary()
                if divisor == 0:
                    raise ValueError("division by zero")
                value = value / divisor
            else:
                return value

    def unary(self):
        tok = self.peek()
        if self.is_op(tok, "-"):
            self.advance()
            return -self.unary()
        if self.is_op(tok, "+"):
            self.advance()
            return self.unary()
        return self.power()

    def power(self):
        base = self.atom()
        if self.is_op(self.peek(), "**"):
            self.advance()
            exponent = self.unary()
            if exponent.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exponent)
            if base == 0 and e < 0:
                raise ValueError("zero cannot be raised to a negative power")
            return base ** e
        return base

    def atom(self):
        tok = self.advance()
        if tok[0] == "num":
            return fractions.Fraction(tok[1])
        if self.is_op(tok, "("):
            value = self.expr()
            closing = self.advance()
            if not self.is_op(closing, ")"):
                raise ValueError("expected ')'")
            return value
        raise ValueError("unexpected token")


def evaluate(s: str) -> fractions.Fraction:
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    tokens = _tokenize(s)
    return _Parser(tokens).parse()
