from fractions import Fraction
import math


def best_approx(x: Fraction, N: int) -> Fraction:
    x = Fraction(x)
    # Candidates: for each denominator q <= N, the nearest numerators are floor(x*q) and ceil(x*q).
    # The best approximation with denominator bound N is among the best lower and upper
    # approximations (in the Stern-Brocot sense) with denominator <= N.
    fl = math.floor(x)
    if x == fl:
        return Fraction(fl, 1)

    # Stern-Brocot search for the closest fraction with denominator <= N.
    # Maintain left bound a/b < x and right bound c/d > x.
    a, b = fl, 1
    c, d = fl + 1, 1

    # Find the best lower bound (largest fraction <= x with denom <= N)
    # and best upper bound (smallest fraction >= x with denom <= N).
    # Use the standard continued-fraction walk.
    lo_p, lo_q = a, b
    hi_p, hi_q = c, d
    while True:
        mp, mq = lo_p + hi_p, lo_q + hi_q
        if mq > N:
            break
        # compare mp/mq with x
        # mp/mq < x  <=> mp*den < num*mq
        if Fraction(mp, mq) < x:
            # move lower bound towards x as far as possible
            # find largest k with (lo + k*hi) < x and denom <= N
            num_x, den_x = x.numerator, x.denominator
            # lo_p + k*hi_p over lo_q + k*hi_q < x
            # (lo_p + k*hi_p)*den_x < num_x*(lo_q + k*hi_q)
            # k*(hi_p*den_x - num_x*hi_q) < num_x*lo_q - lo_p*den_x
            coef = hi_p * den_x - num_x * hi_q  # > 0 since hi > x
            rhs = num_x * lo_q - lo_p * den_x   # > 0 since lo < x
            k = (rhs - 1) // coef  # largest k with k*coef < rhs
            # denominator constraint
            if hi_q > 0:
                k = min(k, (N - lo_q) // hi_q)
            if k < 1:
                k = 1
            lo_p, lo_q = lo_p + k * hi_p, lo_q + k * hi_q
        else:
            num_x, den_x = x.numerator, x.denominator
            # (hi_p + k*lo_p)/(hi_q + k*lo_q) > x
            # (hi_p + k*lo_p)*den_x > num_x*(hi_q + k*lo_q)
            # k*(lo_p*den_x - num_x*lo_q) > num_x*hi_q - hi_p*den_x
            coef = num_x * lo_q - lo_p * den_x  # > 0
            rhs = hi_p * den_x - num_x * hi_q   # > 0
            k = (rhs - 1) // coef
            if lo_q > 0:
                k = min(k, (N - hi_q) // lo_q)
            if k < 1:
                k = 1
            hi_p, hi_q = hi_p + k * lo_p, hi_q + k * lo_q

    lower = Fraction(lo_p, lo_q)
    upper = Fraction(hi_p, hi_q)
    dl = x - lower
    du = upper - x
    if dl < du:
        return lower
    if du < dl:
        return upper
    # tie: smallest denominator, then smaller value
    if lo_q < hi_q:
        return lower
    if hi_q < lo_q:
        return upper
    return lower
