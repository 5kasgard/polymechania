def _seg_match(p: str, s: str) -> bool:
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
    P = pattern.split("/") if pattern != "" else []
    S = path.split("/") if path != "" else []
    n = len(S)
    cur = {0}
    for seg in P:
        if not cur:
            return False
        if seg == "**":
            m = min(cur)
            cur = set(range(m, n + 1))
        else:
            nxt = set()
            for j in cur:
                if j < n and _seg_match(seg, S[j]):
                    nxt.add(j + 1)
            cur = nxt
    return n in cur
