def _seg_match(p, s):
    pi = si = 0
    star = -1
    mark = 0
    lp, ls = len(p), len(s)
    while si < ls:
        if pi < lp and p[pi] == '*':
            star = pi
            mark = si
            pi += 1
        elif pi < lp and (p[pi] == '?' or p[pi] == s[si]):
            pi += 1
            si += 1
        elif star != -1:
            mark += 1
            si = mark
            pi = star + 1
        else:
            return False
    while pi < lp and p[pi] == '*':
        pi += 1
    return pi == lp


def glob_match(pattern: str, path: str) -> bool:
    ps = pattern.split("/") if pattern != "" else []
    xs = path.split("/") if path != "" else []
    m, n = len(ps), len(xs)
    prev = [False] * (n + 1)
    prev[n] = True
    for i in range(m - 1, -1, -1):
        seg = ps[i]
        row = [False] * (n + 1)
        if seg == "**":
            row[n] = prev[n]
            for j in range(n - 1, -1, -1):
                row[j] = prev[j] or row[j + 1]
        else:
            for j in range(n):
                if prev[j + 1] and _seg_match(seg, xs[j]):
                    row[j] = True
        prev = row
    return prev[0]
