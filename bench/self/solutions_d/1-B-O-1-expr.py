import fractions
import re


_TOKEN_RE = re.compile(r"\s*(\d+|\*\*|[-+*/()])")


def _tokenize(s):
    tokens = []
    pos = 0
    s = s.rstrip()
    n = len(s)
    while pos < n:
        m = _TOKEN_RE.match(s, pos)
        if not m or m.end() == pos:
            # allow trailing whitespace only
            if s[pos:].strip() == "":
                break
            raise ValueError("invalid syntax")
        tokens.append(m.group(1))
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

    def parse(self):
        if not self.tokens:
            raise ValueError("empty expression")
        value = self.expr()
        if self.peek() is not None:
            raise ValueError("unexpected token")
        return value

    # expr := term (('+'|'-') term)*
    def expr(self):
        value = self.term()
        while self.peek() in ("+", "-"):
            op = self.advance()
            rhs = self.term()
            value = value + rhs if op == "+" else value - rhs
        return value

    # term := unary (('*'|'/') unary)*
    def term(self):
        value = self.unary()
        while self.peek() in ("*", "/"):
            op = self.advance()
            rhs = self.unary()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ValueError("division by zero")
                value = value / rhs
        return value

    # unary := ('+'|'-') unary | power
    def unary(self):
        if self.peek() in ("+", "-"):
            op = self.advance()
            v = self.unary()
            return -v if op == "-" else v
        return self.power()

    # power := atom ('**' unary)?   (right-assoc; exponent may be signed)
    def power(self):
        base = self.atom()
        if self.peek() == "**":
            self.advance()
            exp = self.unary()
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exp)
            if base == 0 and e < 0:
                raise ValueError("zero to a negative power")
            return base ** e
        return base

    # atom := NUMBER | '(' expr ')'
    def atom(self):
        tok = self.advance()
        if tok == "(":
            value = self.expr()
            if self.advance() != ")":
                raise ValueError("expected ')'")
            return value
        if tok.isdigit():
            return fractions.Fraction(int(tok))
        raise ValueError("unexpected token")


def evaluate(s: str) -> fractions.Fraction:
    if not isinstance(s, str):
        raise ValueError("expression must be a string")
    tokens = _tokenize(s)
    result = _Parser(tokens).parse()
    return fractions.Fraction(result)
