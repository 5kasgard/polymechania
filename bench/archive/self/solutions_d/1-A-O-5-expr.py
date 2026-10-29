import fractions
import re

_TOKEN = re.compile(r"\s*(?:(\d+)|(\*\*|[-+*/()]))")


def _tokenize(s):
    tokens = []
    pos = 0
    s = s.rstrip()
    while pos < len(s):
        m = _TOKEN.match(s, pos)
        if not m or m.end() == pos:
            raise ValueError("syntax error at position %d" % pos)
        if m.group(1) is not None:
            tokens.append(("num", int(m.group(1))))
        else:
            tokens.append(("op", m.group(2)))
        pos = m.end()
    tokens.append(("end", None))
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i]

    def take(self):
        tok = self.tokens[self.i]
        self.i += 1
        return tok

    def expect_op(self, op):
        tok = self.take()
        if tok != ("op", op):
            raise ValueError("expected %r" % op)

    def parse(self):
        value = self.expr()
        if self.peek()[0] != "end":
            raise ValueError("unexpected token")
        return value

    def expr(self):
        value = self.term()
        while self.peek() in (("op", "+"), ("op", "-")):
            op = self.take()[1]
            rhs = self.term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def term(self):
        value = self.unary()
        while self.peek() in (("op", "*"), ("op", "/")):
            op = self.take()[1]
            rhs = self.unary()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ZeroDivisionError("division by zero")
                value = value / rhs
        return value

    def unary(self):
        tok = self.peek()
        if tok == ("op", "-"):
            self.take()
            return -self.unary()
        if tok == ("op", "+"):
            self.take()
            return self.unary()
        return self.power()

    def power(self):
        base = self.atom()
        if self.peek() == ("op", "**"):
            self.take()
            exponent = self.unary()  # allows 2**-1; right-associative via recursion
            if exponent.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exponent)
            if e < 0 and base == 0:
                raise ZeroDivisionError("zero to a negative power")
            return base ** e
        return base

    def atom(self):
        tok = self.take()
        if tok[0] == "num":
            return fractions.Fraction(tok[1])
        if tok == ("op", "("):
            value = self.expr()
            self.expect_op(")")
            return value
        raise ValueError("syntax error")


def evaluate(s: str) -> fractions.Fraction:
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    tokens = _tokenize(s)
    if tokens[0] == ("end", None):
        raise ValueError("empty expression")
    result = _Parser(tokens).parse()
    return fractions.Fraction(result)
