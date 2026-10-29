# NOTE: specification text was not provided (received only "r"); this is a
# placeholder pending the full spec. Exact Gaussian elimination over Fraction.
from fractions import Fraction


def linsolve(A, b):
    n = len(A)
    M = [[Fraction(x) for x in row] + [Fraction(bi)] for row, bi in zip(A, b)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if M[r][col] != 0), None)
        if pivot is None:
            raise ValueError("singular matrix")
        M[col], M[pivot] = M[pivot], M[col]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col] / M[col][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return [M[i][n] / M[i][i] for i in range(n)]
