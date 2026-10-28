from fractions import Fraction


def evaluate(s: str) -> Fraction:
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    prec = {'u+': 3, 'u-': 3, '**': 4, '*': 2, '/': 2, '+': 1, '-': 1}
    ops = []
    vals = []

    def apply(op):
        if op == 'u+' or op == 'u-':
            if not vals:
                raise ValueError("syntax error")
            a = vals.pop()
            vals.append(-a if op == 'u-' else a)
            return
        if len(vals) < 2:
            raise ValueError("syntax error")
        b = vals.pop()
        a = vals.pop()
        if op == '+':
            r = a + b
        elif op == '-':
            r = a - b
        elif op == '*':
            r = a * b
        elif op == '/':
            if b == 0:
                raise ValueError("division by zero")
            r = a / b
        else:
            if b.denominator != 1:
                raise ValueError("non-integer exponent")
            e = b.numerator
            if a == 0:
                if e < 0:
                    raise ValueError("division by zero")
                r = Fraction(1) if e == 0 else Fraction(0)
            elif a == 1:
                r = Fraction(1)
            elif a == -1:
                r = Fraction(1) if e % 2 == 0 else Fraction(-1)
            else:
                r = a ** e
            r = Fraction(r)
        vals.append(r)

    n = len(s)
    i = 0
    expect_operand = True
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if expect_operand:
            if '0' <= c <= '9':
                j = i
                while j < n and '0' <= s[j] <= '9':
                    j += 1
                vals.append(Fraction(int(s[i:j])))
                i = j
                expect_operand = False
            elif c == '+' or c == '-':
                ops.append('u' + c)
                i += 1
            elif c == '(':
                ops.append('(')
                i += 1
            else:
                raise ValueError("syntax error")
        else:
            if c == ')':
                while ops and ops[-1] != '(':
                    apply(ops.pop())
                if not ops:
                    raise ValueError("unbalanced parentheses")
                ops.pop()
                i += 1
            elif c in '+-*/':
                if c == '*' and i + 1 < n and s[i + 1] == '*':
                    op = '**'
                    i += 2
                else:
                    op = c
                    i += 1
                p = prec[op]
                while ops and ops[-1] != '(':
                    t = ops[-1]
                    tp = prec[t]
                    if tp > p or (tp == p and op != '**'):
                        apply(ops.pop())
                    else:
                        break
                ops.append(op)
                expect_operand = True
            else:
                raise ValueError("syntax error")
    if expect_operand:
        raise ValueError("syntax error")
    while ops:
        op = ops.pop()
        if op == '(':
            raise ValueError("unbalanced parentheses")
        apply(op)
    if len(vals) != 1:
        raise ValueError("syntax error")
    return vals[0]
