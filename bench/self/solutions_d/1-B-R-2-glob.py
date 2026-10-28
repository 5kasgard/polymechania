def glob_match(pattern: str, path: str) -> bool:
    pat = pattern.split("/") if pattern != "" else []
    segs = path.split("/") if path != "" else []

    def match_seg(p: str, s: str) -> bool:
        # Iterative wildcard match of one segment: '?' one char, '*' any run.
        # Never crosses '/' because segments contain no '/'.
        pi = si = 0
        star = -1
        mark = 0
        n, m = len(p), len(s)
        while si < m:
            if pi < n and (p[pi] == "?" or (p[pi] != "*" and p[pi] == s[si])):
                pi += 1
                si += 1
            elif pi < n and p[pi] == "*":
                star = pi
                mark = si
                pi += 1
            elif star != -1:
                pi = star + 1
                mark += 1
                si = mark
            else:
                return False
        while pi < n and p[pi] == "*":
            pi += 1
        return pi == n

    # Memoised DP over (pattern index, segment index) to avoid exponential
    # blowup on many "**" segments.
    from functools import lru_cache

    P = len(pat)
    S = len(segs)

    @lru_cache(maxsize=None)
    def go(i: int, j: int) -> bool:
        if i == P:
            return j == S
        if pat[i] == "**":
            # zero segments, or consume one segment and stay on "**"
            if go(i + 1, j):
                return True
            return j < S and go(i, j + 1)
        if j == S:
            return False
        if match_seg(pat[i], segs[j]):
            return go(i + 1, j + 1)
        return False

    return go(0, 0)
