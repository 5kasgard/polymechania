import fractions
import re


_TOKEN_RE = re.compile(r"\s*(?:(\d+)|(\*\*|[-+*/()]))")


def _tokenize(s):
    tokens = []
    pos = 0
    n = len(s)
    while True:
        while pos < n and s[pos].isspace():
            pos += 1
        if pos >= n:
            break
        m = _TOKEN_RE.match(s, pos)
        if not m or m.end() == pos:
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
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def advance(self):
        tok = self.peek()
        self.i += 1
        return tok

    def is_op(self, tok, *ops):
        return tok is not None and tok[0] == "op" and tok[1] in ops

    def parse(self):
        if not self.tokens:
            raise ValueError("empty expression")
        value = self.expr()
        if self.peek() is not None:
            raise ValueError("unexpected token")
        return value

    def expr(self):
        value = self.term()
        while self.is_op(self.peek(), "+", "-"):
            op = self.advance()[1]
            rhs = self.term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def term(self):
        value = self.unary()
        while self.is_op(self.peek(), "*", "/"):
            op = self.advance()[1]
            rhs = self.unary()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ValueError("division by zero")
                value = value / rhs
        return value

    def unary(self):
        if self.is_op(self.peek(), "+", "-"):
            op = self.advance()[1]
            operand = self.unary()
            return -operand if op == "-" else operand
        return self.power()

    def power(self):
        base = self.atom()
        if self.is_op(self.peek(), "**"):
            self.advance()
            exponent = self.unary_for_exponent()
            if exponent.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exponent)
            if base == 0 and e < 0:
                raise ValueError("zero to a negative power")
            return base ** e
        return base

    def unary_for_exponent(self):
        # Right-associative: the exponent is itself a power expression,
        # allowing a signed operand (e.g. 2**-1).
        if self.is_op(self.peek(), "+", "-"):
            op = self.advance()[1]
            operand = self.unary_for_exponent()
            return -operand if op == "-" else operand
        return self.power()

    def atom(self):
        tok = self.peek()
        if tok is None:
            raise ValueError("unexpected end of expression")
        if tok[0] == "num":
            self.advance()
            return fractions.Fraction(tok[1])
        if self.is_op(tok, "("):
            self.advance()
            value = self.expr()
            if not self.is_op(self.peek(), ")"):
                raise ValueError("missing closing parenthesis")
            self.advance()
            return value
        raise ValueError("unexpected token")


def evaluate(s: str) -> fractions.Fraction:
    tokens = _tokenize(s)
    return _Parser(tokens).parse()
