from fractions import Fraction


def _tokenize(s):
    toks = []
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
            toks.append(Fraction(int(s[i:j])))
            i = j
        elif c == '*':
            if i + 1 < n and s[i + 1] == '*':
                toks.append('**')
                i += 2
            else:
                toks.append('*')
                i += 1
        elif c in '+-/()':
            toks.append(c)
            i += 1
        else:
            raise ValueError("bad character")
    return toks


_PREC = {'+': 1, '-': 1, '*': 2, '/': 2, 'u+': 3, 'u-': 3, '**': 4}


def _apply(op, vals):
    try:
        if op == 'u+':
            return
        if op == 'u-':
            vals.append(-vals.pop())
            return
        b = vals.pop()
        a = vals.pop()
    except IndexError:
        raise ValueError("syntax error")
    if op == '+':
        vals.append(a + b)
    elif op == '-':
        vals.append(a - b)
    elif op == '*':
        vals.append(a * b)
    elif op == '/':
        if b == 0:
            raise ValueError("division by zero")
        vals.append(a / b)
    else:
        if b.denominator != 1:
            raise ValueError("non-integer exponent")
        e = b.numerator
        if a == 0:
            if e < 0:
                raise ValueError("division by zero")
            vals.append(Fraction(1 if e == 0 else 0))
        elif a == 1:
            vals.append(Fraction(1))
        elif a == -1:
            vals.append(Fraction(1 if e % 2 == 0 else -1))
        else:
            vals.append(a ** e)


def evaluate(s: str) -> Fraction:
    if not isinstance(s, str):
        raise ValueError("not a string")
    toks = _tokenize(s)
    vals = []
    ops = []
    expect_operand = True
    for t in toks:
        if expect_operand:
            if isinstance(t, Fraction):
                vals.append(t)
                expect_operand = False
            elif t == '(':
                ops.append('(')
            elif t == '+':
                ops.append('u+')
            elif t == '-':
                ops.append('u-')
            else:
                raise ValueError("syntax error")
        else:
            if isinstance(t, Fraction):
                raise ValueError("syntax error")
            if t == ')':
                while ops and ops[-1] != '(':
                    _apply(ops.pop(), vals)
                if not ops:
                    raise ValueError("unbalanced")
                ops.pop()
            elif t == '(':
                raise ValueError("syntax error")
            else:
                p = _PREC[t]
                while ops and ops[-1] != '(':
                    q = _PREC[ops[-1]]
                    if q > p or (q == p and t != '**'):
                        _apply(ops.pop(), vals)
                    else:
                        break
                ops.append(t)
                expect_operand = True
    if expect_operand:
        raise ValueError("syntax error")
    while ops:
        op = ops.pop()
        if op == '(':
            raise ValueError("unbalanced")
        _apply(op, vals)
    if len(vals) != 1:
        raise ValueError("syntax error")
    return vals[0]
