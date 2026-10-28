from fractions import Fraction


def best_approx(x: Fraction, N: int) -> Fraction:
    x = Fraction(x)
    if x.denominator <= N:
        return x
    fl = x.numerator // x.denominator
    f = x - fl
    n, m = f.numerator, f.denominator
    a, b = 0, 1  # lo
    c, d = 1, 0  # hi
    while True:
        moved = False
        # advance lo toward f
        den = c * m - n * d
        k = (n * b - a * m) // den
        if d > 0:
            k = min(k, (N - b) // d)
        if k > 0:
            a += k * c
            b += k * d
            moved = True
        # advance hi toward f
        den = n * b - a * m
        k = (c * m - n * d) // den
        if b > 0:
            k = min(k, (N - d) // b)
        if k > 0:
            c += k * a
            d += k * b
            moved = True
        if not moved:
            break
    lo = Fraction(a, b)
    hi = Fraction(c, d)
    dl = f - lo
    dh = hi - f
    if dl < dh:
        r = lo
    elif dh < dl:
        r = hi
    else:
        r = lo if b <= d else hi
    return r + fl
