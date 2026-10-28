# NOTE: Digits are handled one at a time as lists of ints (Karatsuba over digit lists for large inputs), so no int() conversion of the full strings is used.
def _trim(d):
    i = len(d)
    while i > 1 and d[i - 1] == 0:
        i -= 1
    if i == 0:
        return [0]
    return d[:i]


def _add(x, y):
    n = max(len(x), len(y))
    res = [0] * (n + 1)
    carry = 0
    for i in range(n):
        t = carry
        if i < len(x):
            t += x[i]
        if i < len(y):
            t += y[i]
        res[i] = t % 10
        carry = t // 10
    res[n] = carry
    return _trim(res)


def _sub(x, y):
    # assumes x >= y
    res = [0] * len(x)
    borrow = 0
    for i in range(len(x)):
        t = x[i] - borrow
        if i < len(y):
            t -= y[i]
        if t < 0:
            t += 10
            borrow = 1
        else:
            borrow = 0
        res[i] = t
    return _trim(res)


def _shift(d, k):
    if d == [0]:
        return [0]
    return [0] * k + d


def _school(x, y):
    res = [0] * (len(x) + len(y))
    ly = len(y)
    for i, xi in enumerate(x):
        if xi == 0:
            continue
        carry = 0
        for j in range(ly):
            t = res[i + j] + xi * y[j] + carry
            res[i + j] = t % 10
            carry = t // 10
        k = i + ly
        while carry:
            t = res[k] + carry
            res[k] = t % 10
            carry = t // 10
            k += 1
    return _trim(res)


def _kara(x, y):
    if len(x) < 40 or len(y) < 40:
        return _school(x, y)
    m = max(len(x), len(y)) // 2
    x0 = _trim(x[:m])
    x1 = _trim(x[m:]) if len(x) > m else [0]
    y0 = _trim(y[:m])
    y1 = _trim(y[m:]) if len(y) > m else [0]
    z0 = _kara(x0, y0)
    z2 = _kara(x1, y1)
    z1 = _kara(_add(x0, x1), _add(y0, y1))
    z1 = _sub(_sub(z1, z0), z2)
    res = _add(_add(_shift(z2, 2 * m), _shift(z1, m)), z0)
    return _trim(res)


def multiply(a: str, b: str) -> str:
    neg_a = a.startswith("-")
    neg_b = b.startswith("-")
    sa = a[1:] if neg_a else a
    sb = b[1:] if neg_b else b
    xa = [ord(c) - 48 for c in reversed(sa)]
    xb = [ord(c) - 48 for c in reversed(sb)]
    xa = _trim(xa)
    xb = _trim(xb)
    prod = _kara(xa, xb)
    if prod == [0]:
        return "0"
    digits = "".join(chr(d + 48) for d in reversed(prod))
    if neg_a != neg_b:
        return "-" + digits
    return digits
