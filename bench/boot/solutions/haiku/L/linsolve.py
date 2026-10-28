from fractions import Fraction


def linsolve(A: list[list[int]], b: list[int]):
    m = len(A)
    n = len(A[0])
    M = [[Fraction(v) for v in A[i]] + [Fraction(b[i])] for i in range(m)]

    pivot_cols = []
    row = 0
    for col in range(n):
        if row >= m:
            break
        pr = None
        for r in range(row, m):
            if M[r][col] != 0:
                pr = r
                break
        if pr is None:
            continue
        M[row], M[pr] = M[pr], M[row]
        piv = M[row][col]
        if piv != 1:
            M[row] = [v / piv for v in M[row]]
        for r in range(m):
            if r != row and M[r][col] != 0:
                f = M[r][col]
                M[r] = [M[r][j] - f * M[row][j] for j in range(n + 1)]
        pivot_cols.append(col)
        row += 1

    # Inconsistent if a zero coefficient row has a nonzero right-hand side.
    for r in range(row, m):
        if M[r][n] != 0:
            return ("none", None)

    x = [Fraction(0) for _ in range(n)]
    for i, col in enumerate(pivot_cols):
        x[col] = M[i][n]

    if len(pivot_cols) == n:
        return ("unique", x)
    return ("infinite", x)
