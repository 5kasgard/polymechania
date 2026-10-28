def glob_match(pattern: str, path: str) -> bool:
    pat = pattern.split("/") if pattern != "" else []
    segs = path.split("/") if path != "" else []

    def seg_match(p: str, s: str) -> bool:
        # Match a single segment (no "/" inside either), with ? and * wildcards.
        # Iterative two-pointer matching with backtracking on the last '*'.
        pi = si = 0
        star_pi = -1
        star_si = 0
        while si < len(s):
            if pi < len(p) and (p[pi] == "?" or p[pi] == s[si]):
                pi += 1
                si += 1
            elif pi < len(p) and p[pi] == "*":
                star_pi = pi
                star_si = si
                pi += 1
            elif star_pi != -1:
                pi = star_pi + 1
                star_si += 1
                si = star_si
            else:
                return False
        while pi < len(p) and p[pi] == "*":
            pi += 1
        return pi == len(p)

    # Dynamic programming over (pattern segment index, path segment index).
    n, m = len(pat), len(segs)
    # reach[i][j]: pat[i:] matches segs[j:]
    reach = [[False] * (m + 1) for _ in range(n + 1)]
    reach[n][m] = True
    for i in range(n - 1, -1, -1):
        p = pat[i]
        if p == "**":
            # zero segments, or consume one segment and stay on "**"
            for j in range(m, -1, -1):
                val = reach[i + 1][j]
                if not val and j < m:
                    val = reach[i][j + 1]
                reach[i][j] = val
        else:
            for j in range(m):
                reach[i][j] = reach[i + 1][j + 1] and seg_match(p, segs[j])
    return reach[0][0]
