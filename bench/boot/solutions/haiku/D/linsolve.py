from fractions import Fraction


def linsolve(A: list[list[int]], b: list[int]):
    m = len(A)
    n = len(A[0])
    # Augmented matrix with exact rational entries.
    M = [[Fraction(A[i][j]) for j in range(n)] + [Fraction(b[i])] for i in range(m)]

    pivot_cols = []
    row = 0
    for col in range(n):
        # Find a row at or below `row` with a nonzero entry in this column.
        sel = None
        for r in range(row, m):
            if M[r][col] != 0:
                sel = r
                break
        if sel is None:
            continue
        M[row], M[sel] = M[sel], M[row]
        pivot = M[row][col]
        M[row] = [v / pivot for v in M[row]]
        for r in range(m):
            if r != row and M[r][col] != 0:
                factor = M[r][col]
                M[r] = [M[r][k] - factor * M[row][k] for k in range(n + 1)]
        pivot_cols.append(col)
        row += 1
        if row == m:
            break

    # Inconsistent system: a zero row of coefficients with nonzero right side.
    for r in range(row, m):
        if M[r][n] != 0:
            return ("none", None)

    x = [Fraction(0) for _ in range(n)]
    for i, col in enumerate(pivot_cols):
        x[col] = M[i][n]

    if len(pivot_cols) == n:
        return ("unique", x)
    return ("infinite", x)
