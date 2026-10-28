import fractions
from fractions import Fraction


def best_approx(x: fractions.Fraction, N: int) -> fractions.Fraction:
    if N < 1:
        raise ValueError("N must be at least 1")
    x = Fraction(x)
    n, d = x.numerator, x.denominator
    if d <= N:
        return x

    # Invariant: lo < x < hi, lo and hi have denominators <= N and are
    # neighbours in the Farey sequence of order N once the loop ends.
    f = n // d
    lo_p, lo_q = f, 1
    hi_p, hi_q = f + 1, 1

    while lo_q + hi_q <= N:
        m_p, m_q = lo_p + hi_p, lo_q + hi_q
        if m_p * d < n * m_q:
            # mediant below x: move lo towards hi as far as allowed
            A = n * lo_q - lo_p * d
            B = hi_p * d - n * hi_q
            k = min(A // B, (N - lo_q) // hi_q)
            lo_p, lo_q = lo_p + k * hi_p, lo_q + k * hi_q
        else:
            # mediant above x: move hi towards lo as far as allowed
            A = hi_p * d - n * hi_q
            B = n * lo_q - lo_p * d
            k = min(A // B, (N - hi_q) // lo_q)
            hi_p, hi_q = hi_p + k * lo_p, hi_q + k * lo_q

    lo = Fraction(lo_p, lo_q)
    hi = Fraction(hi_p, hi_q)
    dl = x - lo
    du = hi - x
    if dl < du:
        return lo
    if du < dl:
        return hi
    # tie in distance: smallest denominator, then smaller value
    if lo_q < hi_q:
        return lo
    if hi_q < lo_q:
        return hi
    return lo
