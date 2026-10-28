import fractions
import re

_TOKEN = re.compile(r"\s*(\*\*|[-+*/()]|\d+)")


def _tokenize(s: str) -> list[str]:
    tokens = []
    pos = 0
    s = s.rstrip()
    while pos < len(s):
        m = _TOKEN.match(s, pos)
        if not m:
            raise ValueError(f"unexpected character at position {pos}")
        tokens.append(m.group(1))
        pos = m.end()
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def take(self):
        tok = self.peek()
        if tok is None:
            raise ValueError("unexpected end of input")
        self.i += 1
        return tok

    def parse(self):
        value = self.expr()
        if self.peek() is not None:
            raise ValueError(f"unexpected token {self.peek()!r}")
        return value

    def expr(self):
        value = self.term()
        while self.peek() in ("+", "-"):
            op = self.take()
            rhs = self.term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def term(self):
        value = self.unary()
        while self.peek() in ("*", "/"):
            op = self.take()
            rhs = self.unary()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ZeroDivisionError("division by zero")
                value = value / rhs
        return value

    def unary(self):
        if self.peek() in ("+", "-"):
            op = self.take()
            v = self.unary()
            return v if op == "+" else -v
        return self.power()

    def power(self):
        base = self.atom()
        if self.peek() == "**":
            self.take()
            exp = self.unary()
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exp)
            if base == 0 and e < 0:
                raise ZeroDivisionError("zero to a negative power")
            return base ** e
        return base

    def atom(self):
        tok = self.take()
        if tok == "(":
            value = self.expr()
            if self.take() != ")":
                raise ValueError("expected ')'")
            return value
        if tok.isdigit():
            return fractions.Fraction(int(tok))
        raise ValueError(f"unexpected token {tok!r}")


def evaluate(s: str) -> fractions.Fraction:
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    tokens = _tokenize(s)
    if not tokens:
        raise ValueError("empty expression")
    return _Parser(tokens).parse()
