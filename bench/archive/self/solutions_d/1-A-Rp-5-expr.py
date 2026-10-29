from fractions import Fraction


def _tokenize(s):
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
        elif c.isdigit():
            j = i
            while j < n and s[j].isdigit():
                j += 1
            tokens.append(("NUM", int(s[i:j])))
            i = j
        elif s.startswith("**", i):
            tokens.append(("OP", "**"))
            i += 2
        elif c in "+-*/()":
            tokens.append(("OP", c))
            i += 1
        else:
            raise ValueError(f"unexpected character {c!r}")
    tokens.append(("END", None))
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect_op(self, op):
        tok = self.advance()
        if tok != ("OP", op):
            raise ValueError(f"expected {op!r}")

    def parse(self):
        value = self.expr()
        if self.peek()[0] != "END":
            raise ValueError("unexpected trailing input")
        return value

    def expr(self):
        value = self.term()
        while self.peek() in (("OP", "+"), ("OP", "-")):
            op = self.advance()[1]
            rhs = self.term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def term(self):
        value = self.unary()
        while self.peek() in (("OP", "*"), ("OP", "/")):
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
        if self.peek() in (("OP", "+"), ("OP", "-")):
            op = self.advance()[1]
            operand = self.unary()
            return -operand if op == "-" else operand
        return self.power()

    def power(self):
        base = self.atom()
        if self.peek() == ("OP", "**"):
            self.advance()
            exponent = self.unary()  # right-associative; allows signed exponents
            if exponent.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exponent)
            if base == 0 and e < 0:
                raise ValueError("zero cannot be raised to a negative power")
            return base ** e
        return base

    def atom(self):
        tok = self.advance()
        if tok[0] == "NUM":
            return Fraction(tok[1])
        if tok == ("OP", "("):
            value = self.expr()
            self.expect_op(")")
            return value
        raise ValueError("syntax error")


def evaluate(s: str) -> Fraction:
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    tokens = _tokenize(s)
    if tokens[0][0] == "END":
        raise ValueError("empty expression")
    return _Parser(tokens).parse()
