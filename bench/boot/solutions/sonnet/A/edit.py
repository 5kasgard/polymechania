from array import array


def edit_script(a: str, b: str) -> list[tuple]:
    # trim common prefix and suffix
    p = 0
    la, lb = len(a), len(b)
    while p < la and p < lb and a[p] == b[p]:
        p += 1
    s = 0
    while s < la - p and s < lb - p and a[la - 1 - s] == b[lb - 1 - s]:
        s += 1
    x = a[p:la - s]
    y = b[p:lb - s]
    n, m = len(x), len(y)

    rows = [array('H', range(m + 1))]
    for i in range(1, n + 1):
        ca = x[i - 1]
        prev = rows[-1]
        cur = [i]
        left = i
        for cb, pd, pu in zip(y, prev, prev[1:]):
            d = pd + (ca != cb)
            u = pu + 1
            if u < d:
                d = u
            l = left + 1
            if l < d:
                d = l
            cur.append(d)
            left = d
        rows.append(array('H', cur))

    mid = []
    i, j = n, m
    while i > 0 or j > 0:
        v = rows[i][j]
        if i > 0 and j > 0:
            dg = rows[i - 1][j - 1]
            if x[i - 1] == y[j - 1] and v == dg:
                mid.append(("keep", x[i - 1]))
                i -= 1
                j -= 1
                continue
            if v == dg + 1:
                mid.append(("sub", x[i - 1], y[j - 1]))
                i -= 1
                j -= 1
                continue
        if i > 0 and v == rows[i - 1][j] + 1:
            mid.append(("del", x[i - 1]))
            i -= 1
        else:
            mid.append(("ins", y[j - 1]))
            j -= 1
    mid.reverse()

    res = [("keep", c) for c in a[:p]]
    res.extend(mid)
    res.extend(("keep", c) for c in a[la - s:])
    return res
