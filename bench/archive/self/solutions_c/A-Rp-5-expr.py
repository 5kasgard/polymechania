import fractions
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
            tokens.append(('num', int(s[i:j])))
            i = j
        elif c == '*':
            if i + 1 < n and s[i + 1] == '*':
                tokens.append(('op', '**'))
                i += 2
            else:
                tokens.append(('op', '*'))
                i += 1
        elif c in '+-/()':
            tokens.append(('op', c))
            i += 1
        else:
            raise ValueError("unexpected character %r" % c)
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
        self.pos += 1
        return tok

    def is_op(self, tok, ops):
        return tok is not None and tok[0] == 'op' and tok[1] in ops

    def parse_expr(self):
        value = self.parse_term()
        while self.is_op(self.peek(), ('+', '-')):
            op = self.advance()[1]
            rhs = self.parse_term()
            value = value + rhs if op == '+' else value - rhs
        return value

    def parse_term(self):
        value = self.parse_unary()
        while self.is_op(self.peek(), ('*', '/')):
            op = self.advance()[1]
            rhs = self.parse_unary()
            if op == '*':
                value = value * rhs
            else:
                if rhs == 0:
                    raise ValueError("division by zero")
                value = value / rhs
        return value

    def parse_unary(self):
        if self.is_op(self.peek(), ('+', '-')):
            op = self.advance()[1]
            operand = self.parse_unary()
            return -operand if op == '-' else operand
        return self.parse_power()

    def parse_power(self):
        base = self.parse_atom()
        if self.is_op(self.peek(), ('**',)):
            self.advance()
            exp = self.parse_unary()  # right-assoc, allows 2**-1
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exp)
            if base == 0 and e < 0:
                raise ValueError("division by zero")
            return base ** e
        return base

    def parse_atom(self):
        tok = self.advance()
        if tok is None:
            raise ValueError("unexpected end of input")
        if tok[0] == 'num':
            return Fraction(tok[1])
        if self.is_op(tok, ('(',)):
            value = self.parse_expr()
            closing = self.advance()
            if not self.is_op(closing, (')',)):
                raise ValueError("expected ')'")
            return value
        raise ValueError("unexpected token")


def evaluate(s: str) -> fractions.Fraction:
    tokens = _tokenize(s)
    if not tokens:
        raise ValueError("empty expression")
    parser = _Parser(tokens)
    result = parser.parse_expr()
    if parser.pos != len(tokens):
        raise ValueError("unexpected trailing input")
    return Fraction(result)
