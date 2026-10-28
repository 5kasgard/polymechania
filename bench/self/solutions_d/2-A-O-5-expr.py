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
        elif s.startswith('**', i):
            tokens.append(('op', '**'))
            i += 2
        elif c in '+-*/':
            tokens.append(('op', c))
            i += 1
        elif c == '(' or c == ')':
            tokens.append(('op', c))
            i += 1
        else:
            raise ValueError("unexpected character %r" % c)
    tokens.append(('end', None))
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
        if tok != ('op', op):
            raise ValueError("expected %r" % op)

    def parse(self):
        value = self.parse_expr()
        if self.peek()[0] != 'end':
            raise ValueError("unexpected trailing input")
        return value

    def parse_expr(self):
        value = self.parse_term()
        while self.peek() in (('op', '+'), ('op', '-')):
            op = self.advance()[1]
            rhs = self.parse_term()
            value = value + rhs if op == '+' else value - rhs
        return value

    def parse_term(self):
        value = self.parse_unary()
        while self.peek() in (('op', '*'), ('op', '/')):
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
        tok = self.peek()
        if tok == ('op', '-'):
            self.advance()
            return -self.parse_unary()
        if tok == ('op', '+'):
            self.advance()
            return self.parse_unary()
        return self.parse_power()

    def parse_power(self):
        base = self.parse_atom()
        if self.peek() == ('op', '**'):
            self.advance()
            exp = self.parse_unary()
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = exp.numerator
            if base == 0 and e < 0:
                raise ValueError("zero to a negative power")
            if e >= 0:
                return base ** e
            return Fraction(1) / (base ** (-e))
        return base

    def parse_atom(self):
        tok = self.advance()
        if tok[0] == 'num':
            return Fraction(tok[1])
        if tok == ('op', '('):
            value = self.parse_expr()
            self.expect_op(')')
            return value
        raise ValueError("syntax error")


def evaluate(s: str) -> fractions.Fraction:
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    tokens = _tokenize(s)
    if tokens[0] == ('end', None):
        raise ValueError("empty expression")
    return _Parser(tokens).parse()
