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
            raise ValueError("syntax error at position %d" % pos)
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

    def take(self):
        tok = self.peek()
        if tok is None:
            raise ValueError("unexpected end of input")
        self.i += 1
        return tok

    def expect_op(self, op):
        tok = self.take()
        if tok != ("op", op):
            raise ValueError("expected %r" % op)

    def parse(self):
        if not self.tokens:
            raise ValueError("empty expression")
        value = self.expr()
        if self.peek() is not None:
            raise ValueError("unexpected token")
        return value

    # expr := term (('+' | '-') term)*
    def expr(self):
        value = self.term()
        while True:
            tok = self.peek()
            if tok == ("op", "+"):
                self.i += 1
                value = value + self.term()
            elif tok == ("op", "-"):
                self.i += 1
                value = value - self.term()
            else:
                return value

    # term := unary (('*' | '/') unary)*
    def term(self):
        value = self.unary()
        while True:
            tok = self.peek()
            if tok == ("op", "*"):
                self.i += 1
                value = value * self.unary()
            elif tok == ("op", "/"):
                self.i += 1
                divisor = self.unary()
                if divisor == 0:
                    raise ValueError("division by zero")
                value = value / divisor
            else:
                return value

    # unary := ('+' | '-') unary | power
    def unary(self):
        tok = self.peek()
        if tok == ("op", "-"):
            self.i += 1
            return -self.unary()
        if tok == ("op", "+"):
            self.i += 1
            return self.unary()
        return self.power()

    # power := atom ['**' unary]   (right-associative; exponent may be signed)
    def power(self):
        base = self.atom()
        if self.peek() == ("op", "**"):
            self.i += 1
            exp = self.unary()
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exp)
            if base == 0 and e < 0:
                raise ValueError("division by zero")
            return base ** e
        return base

    # atom := number | '(' expr ')'
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
    tokens = _tokenize(s)
    result = _Parser(tokens).parse()
    return fractions.Fraction(result)
