from fractions import Fraction
import math


def best_approx(x: Fraction, N: int) -> Fraction:
    x = Fraction(x)
    # Candidates: for each denominator q <= N, the nearest numerators
    # floor(x*q) and ceil(x*q). The closest fraction with denominator bound N
    # is among the best rational approximations (continued fraction convergents
    # and semiconvergents). We use the Stern-Brocot / continued fraction walk.

    p0, q0, p1, q1 = 0, 1, 1, 0
    # Work with the floor part and continued fraction expansion of x.
    a_num, a_den = x.numerator, x.denominator
    lower = None  # best lower bound fraction with denom <= N
    upper = None  # best upper bound fraction with denom <= N

    # Standard approach: find the two bounding fractions of x with denominator <= N
    # via the Stern-Brocot descent with batched steps.
    lo_p, lo_q = math.floor(x), 1
    hi_p, hi_q = lo_p + 1, 1
    if x == lo_p:
        return Fraction(lo_p, 1)
    # Use mediant descent with batching.
    # Invariant: lo < x < hi, lo = lo_p/lo_q, hi = hi_p/hi_q.
    while True:
        # Mediant steps towards x.
        # Moving lo up: lo' = lo + k*hi, check if still < x and denom within N.
        # Compute how many steps keep the lower bound < x and denominator <= N.
        # lo + k*hi < x  <=>  (lo_p + k*hi_p)*a_den < a_num*(lo_q + k*hi_q)
        # Solve for max k.
        num_lo = a_num * lo_q - a_den * lo_p   # > 0
        den_lo = a_den * hi_p - a_num * hi_q   # ... see below
        # Bound from denominator: lo_q + k*hi_q <= N
        k_den = (N - lo_q) // hi_q if hi_q else 0
        # Condition lo + k*hi < x:
        # a_den*(lo_p + k*hi_p) < a_num*(lo_q + k*hi_q)
        # k*(a_num*hi_q - a_den*hi_p) > a_den*lo_p - a_num*lo_q
        c = a_num * hi_q - a_den * hi_p   # > 0 since hi > x
        d = a_num * lo_q - a_den * lo_p   # > 0 since lo < x
        # Need k*c > -d, always true for k >= 0; we want largest k with lo+k*hi < x:
        # lo + k*hi <= x  first failing is when lo+k*hi >= x. Let's directly compute.
        # lo_p + k*hi_p < x*(lo_q + k*hi_q)
        # k*(hi_p - x*hi_q) < x*lo_q - lo_p  ->  hi_p - x*hi_q < 0 so k > (x*lo_q-lo_p)/(hi_p-x*hi_q)
        # Actually moving lo upward toward x: lo+k*hi increases in value? It's between lo and hi,
        # decreasing towards hi. Values lo+k*hi approach hi, not x. So we want largest k with lo+k*hi <= x.
        # (lo_p + k*hi_p)*a_den <= a_num*(lo_q + k*hi_q)
        # k*(hi_p*a_den - a_num*hi_q) <= a_num*lo_q - lo_p*a_den
        # With hi_p*a_den - a_num*hi_q = -c < 0: k >= -(d)/c ... i.e. k*(-c) <= d -> always true?
        # Simpler: compare fractions directly with a binary search over k.
        # Find largest k in [0, k_den] with (lo_p+k*hi_p)/(lo_q+k*hi_q) <= x.
        lo_k = 0
        hi_k = k_den
        while lo_k < hi_k:
            mid = (lo_k + hi_k + 1) // 2
            if Fraction(lo_p + mid * hi_p, lo_q + mid * hi_q) <= x:
                lo_k = mid
            else:
                hi_k = mid - 1
        k_lo = lo_k
        if k_lo > 0:
            lo_p, lo_q = lo_p + k_lo * hi_p, lo_q + k_lo * hi_q
        # Now move hi downward toward x: hi' = hi + k*lo, largest k with hi+k*lo >= x.
        k_den = (N - hi_q) // lo_q if lo_q else 0
        lo_k = 0
        hi_k = k_den
        while lo_k < hi_k:
            mid = (lo_k + hi_k + 1) // 2
            if Fraction(hi_p + mid * lo_p, hi_q + mid * lo_q) >= x:
                lo_k = mid
            else:
                hi_k = mid - 1
        k_hi = lo_k
        if k_hi > 0:
            hi_p, hi_q = hi_p + k_hi * lo_p, hi_q + k_hi * lo_q
        if k_lo == 0 and k_hi == 0:
            break

    lower = Fraction(lo_p, lo_q)
    upper = Fraction(hi_p, hi_q)
    if lower == x:
        return lower
    if upper == x:
        return upper
    dl = x - lower
    du = upper - x
    if dl < du:
        return lower
    if du < dl:
        return upper
    # Tie: smallest denominator, then smaller value.
    if lo_q < hi_q:
        return lower
    if hi_q < lo_q:
        return upper
    return lower
