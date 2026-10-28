from fractions import Fraction


def best_approx(x: Fraction, N: int) -> Fraction:
    x = Fraction(x)
    if x.denominator <= N:
        return x
    n = x.numerator // x.denominator
    f = x - n
    P, Q = f.numerator, f.denominator
    a, b, c, d = 0, 1, 1, 1
    while b + d <= N:
        ma, mb = a + c, b + d
        if ma * Q < P * mb:
            # move lo toward hi
            k = (P * b - Q * a - 1) // (Q * c - P * d)
            k = min(k, (N - b) // d)
            a, b = a + k * c, b + k * d
        else:
            k = (Q * c - P * d - 1) // (P * b - Q * a)
            k = min(k, (N - d) // b)
            c, d = c + k * a, d + k * b
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
    return r + n
