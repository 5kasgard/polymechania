from fractions import Fraction


def linsolve(A: list[list[int]], b: list[int]):
    m = len(A)
    n = len(A[0])
    # Augmented matrix with exact rational entries.
    M = [[Fraction(A[i][j]) for j in range(n)] + [Fraction(b[i])] for i in range(m)]

    pivot_cols = []
    row = 0
    for col in range(n):
        if row >= m:
            break
        pivot = None
        for r in range(row, m):
            if M[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        M[row], M[pivot] = M[pivot], M[row]
        p = M[row][col]
        if p != 1:
            M[row] = [v / p for v in M[row]]
        for r in range(m):
            if r != row and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * c for a, c in zip(M[r], M[row])]
        pivot_cols.append(col)
        row += 1

    # Rows without a pivot must have zero right-hand side for consistency.
    for r in range(len(pivot_cols), m):
        if M[r][n] != 0:
            return ("none", None)

    x = [Fraction(0) for _ in range(n)]
    for i, col in enumerate(pivot_cols):
        x[col] = M[i][n]

    if len(pivot_cols) == n:
        return ("unique", x)
    return ("infinite", x)
