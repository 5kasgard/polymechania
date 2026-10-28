from array import array


def edit_script(a: str, b: str) -> list[tuple]:
    p = 0
    lim = min(len(a), len(b))
    while p < lim and a[p] == b[p]:
        p += 1
    s = 0
    while s < lim - p and a[len(a) - 1 - s] == b[len(b) - 1 - s]:
        s += 1
    x = a[p:len(a) - s]
    y = b[p:len(b) - s]
    n, m = len(x), len(y)

    rows = [array('H', range(m + 1))]
    for i in range(1, n + 1):
        prev = rows[-1]
        cur = [i] * (m + 1)
        xc = x[i - 1]
        left = i
        for j in range(1, m + 1):
            if xc == y[j - 1]:
                v = prev[j - 1]
            else:
                v = prev[j - 1] + 1
                t = prev[j] + 1
                if t < v:
                    v = t
                t = left + 1
                if t < v:
                    v = t
            cur[j] = v
            left = v
        rows.append(array('H', cur))

    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            cv = rows[i][j]
            if x[i - 1] == y[j - 1] and cv == rows[i - 1][j - 1]:
                ops.append(("keep", x[i - 1]))
                i -= 1
                j -= 1
                continue
            if x[i - 1] != y[j - 1] and cv == rows[i - 1][j - 1] + 1:
                ops.append(("sub", x[i - 1], y[j - 1]))
                i -= 1
                j -= 1
                continue
        if i > 0 and rows[i][j] == rows[i - 1][j] + 1:
            ops.append(("del", x[i - 1]))
            i -= 1
        else:
            ops.append(("ins", y[j - 1]))
            j -= 1
    ops.reverse()

    res = [("keep", c) for c in a[:p]]
    res.extend(ops)
    res.extend(("keep", c) for c in a[len(a) - s:])
    return res
