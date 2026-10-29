import fractions
import re


_TOKEN_RE = re.compile(r"\s*(?:(\d+)|(\*\*|[-+*/()]))")


def _tokenize(s):
    tokens = []
    pos = 0
    n = len(s)
    while pos < n:
        if s[pos].isspace():
            pos += 1
            continue
        m = _TOKEN_RE.match(s, pos)
        if not m:
            raise ValueError("invalid character at position %d" % pos)
        if m.group(1) is not None:
            tokens.append(("num", int(m.group(1))))
        else:
            tokens.append(("op", m.group(2)))
        pos = m.end()
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        tok = self.peek()
        if tok is None:
            raise ValueError("unexpected end of input")
        self.pos += 1
        return tok

    def is_op(self, tok, value):
        return tok is not None and tok[0] == "op" and tok[1] == value

    def parse(self):
        value = self.parse_expr()
        if self.peek() is not None:
            raise ValueError("unexpected token")
        return value

    # expr := term (('+' | '-') term)*
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

    # term := unary (('*' | '/') unary)*
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

    # unary := ('+' | '-') unary | power
    def parse_unary(self):
        tok = self.peek()
        if self.is_op(tok, "-"):
            self.advance()
            return -self.parse_unary()
        if self.is_op(tok, "+"):
            self.advance()
            return self.parse_unary()
        return self.parse_power()

    # power := primary ('**' unary)?   (right-associative, exponent may be signed)
    def parse_power(self):
        base = self.parse_primary()
        if self.is_op(self.peek(), "**"):
            self.advance()
            exponent = self.parse_unary()
            if exponent.denominator != 1:
                raise ValueError("exponent is not an integer")
            e = exponent.numerator
            if base == 0 and e < 0:
                raise ValueError("zero cannot be raised to a negative power")
            if e >= 0:
                return base ** e
            return fractions.Fraction(1) / (base ** (-e))
        return base

    # primary := number | '(' expr ')'
    def parse_primary(self):
        tok = self.advance()
        if tok[0] == "num":
            return fractions.Fraction(tok[1])
        if self.is_op(tok, "("):
            value = self.parse_expr()
            if not self.is_op(self.peek(), ")"):
                raise ValueError("expected ')'")
            self.advance()
            return value
        raise ValueError("unexpected token")


def evaluate(s: str) -> fractions.Fraction:
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    tokens = _tokenize(s)
    if not tokens:
        raise ValueError("empty expression")
    return _Parser(tokens).parse()
