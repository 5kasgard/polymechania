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
            tokens.append(("num", int(s[i:j])))
            i = j
        elif c == "*":
            if i + 1 < n and s[i + 1] == "*":
                tokens.append(("op", "**"))
                i += 2
            else:
                tokens.append(("op", "*"))
                i += 1
        elif c in "+-/()":
            tokens.append(("op", c))
            i += 1
        else:
            raise ValueError("unexpected character %r" % c)
    tokens.append(("end", None))
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
        if self.peek() in (("op", "+"), ("op", "-")):
            op = self.advance()[1]
            value = self.parse_unary()
            return -value if op == "-" else value
        return self.parse_power()

    # power := primary ('**' unary)?   (right-associative; exponent may be signed)
    def parse_power(self):
        base = self.parse_primary()
        if self.peek() == ("op", "**"):
            self.advance()
            exp = self.parse_unary()
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exp)
            if base == 0 and e < 0:
                raise ValueError("zero to a negative power")
            return base ** e
        return base

    # primary := NUMBER | '(' expr ')'
    def parse_primary(self):
        tok = self.advance()
        if tok[0] == "num":
            return Fraction(tok[1])
        if tok == ("op", "("):
            value = self.parse_expr()
            self.expect_op(")")
            return value
        raise ValueError("unexpected token")


def evaluate(s: str) -> Fraction:
    tokens = _tokenize(s)
    parser = _Parser(tokens)
    result = parser.parse_expr()
    if parser.peek()[0] != "end":
        raise ValueError("trailing input")
    return Fraction(result)
