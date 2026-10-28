from fractions import Fraction


def _tokenize(s):
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
        elif '0' <= c <= '9':
            j = i
            while j < n and '0' <= s[j] <= '9':
                j += 1
            tokens.append(('NUM', int(s[i:j])))
            i = j
        elif c == '*':
            if i + 1 < n and s[i + 1] == '*':
                tokens.append(('OP', '**'))
                i += 2
            else:
                tokens.append(('OP', '*'))
                i += 1
        elif c in '+-/()':
            tokens.append(('OP', c))
            i += 1
        else:
            raise ValueError("invalid character: %r" % c)
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek_op(self):
        if self.pos < len(self.tokens):
            kind, val = self.tokens[self.pos]
            if kind == 'OP':
                return val
        return None

    def advance(self):
        self.pos += 1

    def parse_expr(self):
        v = self.parse_term()
        while True:
            op = self.peek_op()
            if op == '+':
                self.advance()
                v = v + self.parse_term()
            elif op == '-':
                self.advance()
                v = v - self.parse_term()
            else:
                return v

    def parse_term(self):
        v = self.parse_unary()
        while True:
            op = self.peek_op()
            if op == '*':
                self.advance()
                v = v * self.parse_unary()
            elif op == '/':
                self.advance()
                r = self.parse_unary()
                if r == 0:
                    raise ValueError("division by zero")
                v = v / r
            else:
                return v

    def parse_unary(self):
        negative = False
        while True:
            op = self.peek_op()
            if op == '-':
                negative = not negative
                self.advance()
            elif op == '+':
                self.advance()
            else:
                break
        v = self.parse_power()
        return -v if negative else v

    def parse_power(self):
        base = self.parse_atom()
        if self.peek_op() == '**':
            self.advance()
            exp = self.parse_unary()
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exp.numerator)
            if e < 0 and base == 0:
                raise ValueError("zero cannot be raised to a negative power")
            return base ** e
        return base

    def parse_atom(self):
        if self.pos >= len(self.tokens):
            raise ValueError("unexpected end of input")
        kind, val = self.tokens[self.pos]
        if kind == 'NUM':
            self.advance()
            return Fraction(val)
        if kind == 'OP' and val == '(':
            self.advance()
            v = self.parse_expr()
            if self.peek_op() != ')':
                raise ValueError("expected ')'")
            self.advance()
            return v
        raise ValueError("unexpected token: %r" % (val,))


def evaluate(s: str) -> Fraction:
    tokens = _tokenize(s)
    if not tokens:
        raise ValueError("empty expression")
    parser = _Parser(tokens)
    result = parser.parse_expr()
    if parser.pos != len(tokens):
        raise ValueError("unexpected trailing input")
    return Fraction(result)
