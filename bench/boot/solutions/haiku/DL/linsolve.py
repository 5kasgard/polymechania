from fractions import Fraction


def linsolve(A: list[list[int]], b: list[int]):
    m = len(A)
    n = len(A[0])
    # augmented matrix with Fraction entries
    M = [[Fraction(A[i][j]) for j in range(n)] + [Fraction(b[i])] for i in range(m)]

    pivot_cols = []
    row = 0
    for col in range(n):
        if row >= m:
            break
        sel = None
        for r in range(row, m):
            if M[r][col] != 0:
                sel = r
                break
        if sel is None:
            continue
        M[row], M[sel] = M[sel], M[row]
        pv = M[row][col]
        M[row] = [v / pv for v in M[row]]
        for r in range(m):
            if r != row and M[r][col] != 0:
                f = M[r][col]
                M[r] = [M[r][k] - f * M[row][k] for k in range(n + 1)]
        pivot_cols.append(col)
        row += 1

    # inconsistency: a zero coefficient row with nonzero right-hand side
    for r in range(row, m):
        if M[r][n] != 0:
            return ("none", None)

    if len(pivot_cols) == n:
        x = [Fraction(0)] * n
        for i, col in enumerate(pivot_cols):
            x[col] = M[i][n]
        return ("unique", x)

    x = [Fraction(0)] * n
    for i, col in enumerate(pivot_cols):
        x[col] = M[i][n]
    return ("infinite", x)
