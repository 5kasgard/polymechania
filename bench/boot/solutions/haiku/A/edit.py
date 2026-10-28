from array import array


def edit_script(a: str, b: str) -> list[tuple]:
    # Strip the common prefix and suffix: matching them is always optimal.
    n_full, m_full = len(a), len(b)
    p = 0
    lim = min(n_full, m_full)
    while p < lim and a[p] == b[p]:
        p += 1
    s = 0
    while s < lim - p and a[n_full - 1 - s] == b[m_full - 1 - s]:
        s += 1

    head = [("keep", a[k]) for k in range(p)]
    tail = [("keep", a[n_full - s + k]) for k in range(s)]

    x = a[p:n_full - s]
    y = b[p:m_full - s]
    n, m = len(x), len(y)

    if n == 0 and m == 0:
        return head + tail

    # dp[i][j] = Levenshtein distance between x[:i] and y[:j]
    dp = [array('H', range(m + 1))]
    for i in range(1, n + 1):
        prev = dp[-1]
        cur = [i] + [0] * m
        xi = x[i - 1]
        for j in range(1, m + 1):
            best = prev[j] + 1
            t = cur[j - 1] + 1
            if t < best:
                best = t
            t = prev[j - 1] + (0 if xi == y[j - 1] else 1)
            if t < best:
                best = t
            cur[j] = best
        dp.append(array('H', cur))

    # Backtrack from (n, m); tie order: keep, sub, del, ins.
    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        d = dp[i][j]
        if i > 0 and j > 0 and x[i - 1] == y[j - 1] and dp[i - 1][j - 1] == d:
            ops.append(("keep", x[i - 1]))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i - 1][j - 1] + 1 == d:
            ops.append(("sub", x[i - 1], y[j - 1]))
            i -= 1
            j -= 1
        elif i > 0 and dp[i - 1][j] + 1 == d:
            ops.append(("del", x[i - 1]))
            i -= 1
        else:
            ops.append(("ins", y[j - 1]))
            j -= 1
    ops.reverse()

    return head + ops + tail
