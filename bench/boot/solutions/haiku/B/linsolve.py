from fractions import Fraction


def linsolve(A: list[list[int]], b: list[int]):
    m = len(A)
    n = len(A[0])
    # Augmented matrix over the rationals; the input lists are not modified.
    M = [[Fraction(v) for v in row] + [Fraction(b[i])] for i, row in enumerate(A)]
    pivots = []
    r = 0
    for c in range(n):
        if r == m:
            break
        p = None
        for i in range(r, m):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = Fraction(1) / M[r][c]
        M[r] = [v * inv for v in M[r]]
        pivot_row = M[r]
        for i in range(m):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * q for a, q in zip(M[i], pivot_row)]
        pivots.append(c)
        r += 1

    # Rows from r onward have zero coefficients; a nonzero right-hand side means no solution.
    for i in range(r, m):
        if M[i][n] != 0:
            return ("none", None)

    x = [Fraction(0)] * n
    for i, c in enumerate(pivots):
        x[c] = M[i][n]

    if len(pivots) < n:
        return ("infinite", x)
    return ("unique", x)
