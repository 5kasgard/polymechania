def edit_script(a: str, b: str) -> list[tuple]:
    n = len(a)
    m = len(b)
    W = m + 1
    # dirs[i*W + j]: 0 = keep (match diagonal), 1 = sub (diagonal),
    # 2 = del (from above), 3 = ins (from left)
    dirs = bytearray((n + 1) * W)
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        ai = a[i - 1]
        cur = [i] + [0] * m
        base = i * W
        for j in range(1, m + 1):
            bj = b[j - 1]
            if ai == bj:
                diag = prev[j - 1]
                dcode = 0
            else:
                diag = prev[j - 1] + 1
                dcode = 1
            up = prev[j] + 1
            left = cur[j - 1] + 1
            if diag <= up and diag <= left:
                cur[j] = diag
                dirs[base + j] = dcode
            elif up <= left:
                cur[j] = up
                dirs[base + j] = 2
            else:
                cur[j] = left
                dirs[base + j] = 3
        prev = cur

    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        if i == 0:
            ops.append(("ins", b[j - 1]))
            j -= 1
        elif j == 0:
            ops.append(("del", a[i - 1]))
            i -= 1
        else:
            d = dirs[i * W + j]
            if d == 0:
                ops.append(("keep", a[i - 1]))
                i -= 1
                j -= 1
            elif d == 1:
                ops.append(("sub", a[i - 1], b[j - 1]))
                i -= 1
                j -= 1
            elif d == 2:
                ops.append(("del", a[i - 1]))
                i -= 1
            else:
                ops.append(("ins", b[j - 1]))
                j -= 1
    ops.reverse()
    return ops
