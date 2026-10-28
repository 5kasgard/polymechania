def glob_match(pattern: str, path: str) -> bool:
    pat = pattern.split("/") if pattern != "" else []
    segs = path.split("/") if path != "" else []

    def seg_match(p: str, s: str) -> bool:
        # Iterative wildcard match within a single segment:
        # '?' matches one char, '*' matches any run (possibly empty).
        pi = si = 0
        star_p = -1
        star_s = -1
        while si < len(s):
            if pi < len(p) and (p[pi] == "?" or p[pi] == s[si]):
                pi += 1
                si += 1
            elif pi < len(p) and p[pi] == "*":
                star_p = pi
                star_s = si
                pi += 1
            elif star_p != -1:
                pi = star_p + 1
                star_s += 1
                si = star_s
            else:
                return False
        while pi < len(p) and p[pi] == "*":
            pi += 1
        return pi == len(p)

    # Dynamic programming over (pattern segment index, path segment index),
    # with "**" consuming zero or more whole segments.
    n, m = len(pat), len(segs)
    memo = {}

    def go(i: int, j: int) -> bool:
        key = (i, j)
        if key in memo:
            return memo[key]
        if i == n:
            res = j == m
        elif pat[i] == "**":
            res = go(i + 1, j) or (j < m and go(i, j + 1))
        else:
            res = (j < m and seg_match(pat[i], segs[j]) and go(i + 1, j + 1))
        memo[key] = res
        return res

    # Iterative fill to avoid deep recursion on long paths.
    # Compute table bottom-up.
    table = [[False] * (m + 1) for _ in range(n + 1)]
    table[n][m] = True
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n:
                if j != m:
                    table[i][j] = False
                continue
            if pat[i] == "**":
                table[i][j] = table[i + 1][j] or (j < m and table[i][j + 1])
            else:
                table[i][j] = (
                    j < m
                    and seg_match(pat[i], segs[j])
                    and table[i + 1][j + 1]
                )
    return table[0][0]
