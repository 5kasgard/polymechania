from fractions import Fraction
import re

_TOKEN_RE = re.compile(r"\s*(?:(\*\*)|(\d+)|([+\-*/()]))")


def _tokenize(s: str):
    tokens = []
    pos = 0
    n = len(s)
    while pos < n:
        if s[pos:].strip() == "":
            break
        m = _TOKEN_RE.match(s, pos)
        if not m or m.end() == pos:
            raise ValueError("unexpected character in expression")
        if m.group(1):
            tokens.append("**")
        elif m.group(2):
            tokens.append(int(m.group(2)))
        else:
            tokens.append(m.group(3))
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
            operand = self.unary()
            return -operand if op == "-" else operand
        return self.power()

    # power := primary ('**' unary)?   (right-associative, exponent may be unary)
    def power(self):
        base = self.primary()
        if self.peek() == "**":
            self.advance()
            exp = self.unary()
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exp)
            if e >= 0:
                return base ** e
            if base == 0:
                raise ValueError("division by zero")
            return Fraction(1) / (base ** (-e))
        return base

    # primary := INT | '(' expr ')'
    def primary(self):
        tok = self.advance()
        if isinstance(tok, int):
            return Fraction(tok)
        if tok == "(":
            value = self.expr()
            if self.advance() != ")":
                raise ValueError("expected ')'")
            return value
        raise ValueError("syntax error")


def evaluate(s: str) -> Fraction:
    if not isinstance(s, str):
        raise ValueError("expression must be a string")
    tokens = _tokenize(s)
    return _Parser(tokens).parse()
