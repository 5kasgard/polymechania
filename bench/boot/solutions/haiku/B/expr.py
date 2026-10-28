import fractions
from fractions import Fraction


def _tokenize(s):
    toks = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if '0' <= c <= '9':
            j = i
            while j < n and '0' <= s[j] <= '9':
                j += 1
            toks.append(('num', int(s[i:j])))
            i = j
            continue
        if s.startswith('**', i):
            toks.append(('op', '**'))
            i += 2
            continue
        if c in '+-*/()':
            toks.append(('op', c))
            i += 1
            continue
        raise ValueError("invalid character: %r" % c)
    return toks


def evaluate(s: str) -> fractions.Fraction:
    if not isinstance(s, str):
        raise ValueError("expression must be a string")
    toks = _tokenize(s)
    if not toks:
        raise ValueError("empty expression")
    state = {'p': 0}

    def peek():
        p = state['p']
        return toks[p] if p < len(toks) else None

    def is_op(tok, ops):
        return tok is not None and tok[0] == 'op' and tok[1] in ops

    def advance():
        tok = toks[state['p']]
        state['p'] += 1
        return tok

    def parse_expr():
        v = parse_term()
        while is_op(peek(), ('+', '-')):
            op = advance()[1]
            rhs = parse_term()
            v = v + rhs if op == '+' else v - rhs
        return v

    def parse_term():
        v = parse_unary()
        while is_op(peek(), ('*', '/')):
            op = advance()[1]
            rhs = parse_unary()
            if op == '*':
                v = v * rhs
            else:
                if rhs == 0:
                    raise ValueError("division by zero")
                v = v / rhs
        return v

    def parse_unary():
        sign_neg = False
        while is_op(peek(), ('+', '-')):
            if advance()[1] == '-':
                sign_neg = not sign_neg
        v = parse_power()
        return -v if sign_neg else v

    def parse_power():
        base = parse_atom()
        if is_op(peek(), ('**',)):
            advance()
            exp = parse_unary()
            if exp.denominator != 1:
                raise ValueError("exponent must be an integer")
            e = int(exp)
            if base == 0 and e < 0:
                raise ValueError("division by zero")
            return base ** e
        return base

    def parse_atom():
        tok = peek()
        if tok is None:
            raise ValueError("unexpected end of expression")
        if tok[0] == 'num':
            advance()
            return Fraction(tok[1])
        if is_op(tok, ('(',)):
            advance()
            v = parse_expr()
            if not is_op(peek(), (')',)):
                raise ValueError("expected ')'")
            advance()
            return v
        raise ValueError("unexpected token")

    result = parse_expr()
    if state['p'] != len(toks):
        raise ValueError("unexpected trailing input")
    return Fraction(result)
