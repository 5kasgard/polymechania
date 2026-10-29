# NOTE: The work order body is only the single letter "r", so the
# specification for 'approx' is missing. Best effort below: a function
# named 'approx' that accepts a rational number and returns a simple
# rational approximation. Replace with the real specification when it
# arrives.
from fractions import Fraction


def approx(x, max_denominator=1000):
    """Return the best rational approximation to x with denominator <= max_denominator."""
    x = Fraction(x)
    if max_denominator < 1:
        raise ValueError("max_denominator must be at least 1")
    if x.denominator <= max_denominator:
        return x
    p0, q0, p1, q1 = 0, 1, 1, 0
    n, d = x.numerator, x.denominator
    while True:
        a = n // d
        q2 = q0 + a * q1
        if q2 > max_denominator:
            break
        p0, q0, p1, q1 = p1, q1, p0 + a * p1, q2
        n, d = d, n - a * d
        if d == 0:
            break
    k = (max_denominator - q0) // q1 if q1 else 0
    bound1 = Fraction(p0 + k * p1, q0 + k * q1) if (q0 + k * q1) else None
    bound2 = Fraction(p1, q1) if q1 else None
    candidates = [c for c in (bound1, bound2) if c is not None]
    return min(candidates, key=lambda c: abs(c - x))
