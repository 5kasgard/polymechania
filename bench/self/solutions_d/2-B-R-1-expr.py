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

    def take(self):
        tok = self.peek()
        if tok is None:
            raise ValueError("unexpected end of input")
        self.i += 1
        return tok

    def is_op(self, tok, *ops):
        return tok is not None and tok[0] == "op" and tok[1] in ops

    def parse(self):
        value = self.expr()
        if self.peek() is not None:
            raise ValueError("unexpected token")
        return value

    # expr := term (('+' | '-') term)*
    def expr(self):
        value = self.term()
        while self.is_op(self.peek(), "+", "-"):
            op = self.take()[1]
            rhs = self.term()
            value = value + rhs if op == "+" else value - rhs
        return value

    # term := unary (('*' | '/') unary)*
    def term(self):
        value = self.unary()
        while self.is_op(self.peek(), "*", "/"):
            op = self.take()[1]
            rhs = self.unary()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ValueError("division by zero")
                value = value / rhs
        return value

    # unary := ('+' | '-') unary | power
    def unary(self):
        if self.is_op(self.peek(), "+", "-"):
            op = self.take()[1]
            v = self.unary()
            return -v if op == "-" else v
        return self.power()

    # power := atom ('**' unary)?   (right-assoc; exponent may carry a sign)
    def power(self):
        base = self.atom()
        if self.is_op(self.peek(), "**"):
            self.take()
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
        if tok[1] == "(":
            value = self.expr()
            closing = self.take()
            if not self.is_op(closing, ")"):
                raise ValueError("expected ')'")
            return value
        raise ValueError("unexpected token")


def evaluate(s: str) -> fractions.Fraction:
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    tokens = _tokenize(s)
    if not tokens:
        raise ValueError("empty expression")
    result = _Parser(tokens).parse()
    return fractions.Fraction(result)
