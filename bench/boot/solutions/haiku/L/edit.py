def edit_script(a: str, b: str) -> list[tuple]:
    n = len(a)
    m = len(b)

    # D[i][j] = Levenshtein distance between a[:i] and b[:j]
    D = [list(range(m + 1))]
    for i in range(1, n + 1):
        prev = D[i - 1]
        cur = [i] + [0] * m
        ai = a[i - 1]
        for j in range(1, m + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1]
            else:
                x = prev[j - 1]
                y = prev[j]
                z = cur[j - 1]
                if y < x:
                    x = y
                if z < x:
                    x = z
                cur[j] = x + 1
        D.append(cur)

    # Traceback from (n, m) to (0, 0), collecting operations in reverse.
    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1] and D[i][j] == D[i - 1][j - 1]:
            ops.append(("keep", a[i - 1]))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + 1:
            ops.append(("sub", a[i - 1], b[j - 1]))
            i -= 1
            j -= 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            ops.append(("del", a[i - 1]))
            i -= 1
        else:
            ops.append(("ins", b[j - 1]))
            j -= 1

    ops.reverse()
    return ops
