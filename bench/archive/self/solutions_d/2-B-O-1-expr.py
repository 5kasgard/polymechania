import fractions
import re

_TOKEN_RE = re.compile(r"\s*(?:(\d+)|(\*\*|[+\-*/()]))")


def _tokenize(s):
    tokens = []
    pos = 0
    s = s.rstrip()
    while pos < len(s):
        m = _TOKEN_RE.match(s, pos)
        if not m:
            raise ValueError("invalid syntax at position %d" % pos)
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

    def advance(self):
        tok = self.tokens[self.i]
        self.i += 1
        return tok

    def expect_op(self, op):
        tok = self.advance()
        if tok != ("op", op):
            raise ValueError("expected %r" % op)

    # expr := term (('+' | '-') term)*
    def parse_expr(self):
        value = self.parse_term()
        while self.peek() in (("op", "+"), ("op", "-")):
            op = self.advance()[1]
            rhs = self.parse_term()
            value = value + rhs if op == "+" else value - rhs
        return value

    # term := unary (('*' | '/') unary)*
    def parse_term(self):
        value = self.parse_unary()
        while self.peek() in (("op", "*"), ("op", "/")):
            op = self.advance()[1]
            rhs = self.parse_unary()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ValueError("division by zero")
                value = value / rhs
        return value

    # unary := ('+' | '-') unary | power
    def parse_unary(self):
        if self.peek() == ("op", "-"):
            self.advance()
            return -self.parse_unary()
        if self.peek() == ("op", "+"):
            self.advance()
            return self.parse_unary()
        return self.parse_power()

    # power := atom ('**' unary)?   (right-associative; exponent may be signed)
    def parse_power(self):
        base = self.parse_atom()
        if self.peek() == ("op", "**"):
            self.advance()
            exp = self.parse_unary()
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exp)
            if base == 0 and e < 0:
                raise ValueError("division by zero")
            return base ** e
        return base

    # atom := number | '(' expr ')'
    def parse_atom(self):
        tok = self.advance()
        if tok[0] == "num":
            return fractions.Fraction(tok[1])
        if tok == ("op", "("):
            value = self.parse_expr()
            self.expect_op(")")
            return value
        raise ValueError("unexpected token")


def evaluate(s: str) -> fractions.Fraction:
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    tokens = _tokenize(s)
    if tokens == [("end", None)]:
        raise ValueError("empty expression")
    parser = _Parser(tokens)
    result = parser.parse_expr()
    if parser.peek() != ("end", None):
        raise ValueError("unexpected trailing input")
    return fractions.Fraction(result)
