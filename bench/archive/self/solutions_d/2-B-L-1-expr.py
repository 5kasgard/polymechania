import fractions
import re


_TOKEN_RE = re.compile(r"\s*(?:(\d+)|(\*\*|[+\-*/()]))")


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

    # expr := term (('+'|'-') term)*
    def parse_expr(self):
        value = self.parse_term()
        while self.is_op(self.peek(), "+", "-"):
            op = self.take()[1]
            rhs = self.parse_term()
            value = value + rhs if op == "+" else value - rhs
        return value

    # term := unary (('*'|'/') unary)*
    def parse_term(self):
        value = self.parse_unary()
        while self.is_op(self.peek(), "*", "/"):
            op = self.take()[1]
            rhs = self.parse_unary()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ValueError("division by zero")
                value = value / rhs
        return value

    # unary := ('+'|'-') unary | power
    def parse_unary(self):
        if self.is_op(self.peek(), "+", "-"):
            op = self.take()[1]
            v = self.parse_unary()
            return -v if op == "-" else v
        return self.parse_power()

    # power := atom ['**' unary]   (right-assoc; exponent may carry unary sign)
    def parse_power(self):
        base = self.parse_atom()
        if self.is_op(self.peek(), "**"):
            self.take()
            exp = self.parse_unary()
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exp)
            if base == 0 and e < 0:
                raise ValueError("division by zero")
            return base ** e
        return base

    # atom := number | '(' expr ')'
    def parse_atom(self):
        tok = self.take()
        if tok[0] == "num":
            return fractions.Fraction(tok[1])
        if tok[1] == "(":
            value = self.parse_expr()
            closing = self.take()
            if not self.is_op(closing, ")"):
                raise ValueError("expected ')'")
            return value
        raise ValueError("unexpected token %r" % (tok[1],))


def evaluate(s: str) -> fractions.Fraction:
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    tokens = _tokenize(s)
    if not tokens:
        raise ValueError("empty expression")
    parser = _Parser(tokens)
    result = parser.parse_expr()
    if parser.peek() is not None:
        raise ValueError("unexpected trailing input")
    return fractions.Fraction(result)
