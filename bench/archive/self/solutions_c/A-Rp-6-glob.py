def glob_match(pattern: str, path: str) -> bool:
    pat_segs = pattern.split("/") if pattern != "" else []
    path_segs = path.split("/") if path != "" else []

    def seg_match(p: str, s: str) -> bool:
        # Character-level match within a single segment.
        # Dynamic programming over (i in p, j in s).
        n, m = len(p), len(s)
        dp = [[False] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = True
        for i in range(1, n + 1):
            if p[i - 1] == "*":
                dp[i][0] = dp[i - 1][0]
        for i in range(1, n + 1):
            pc = p[i - 1]
            for j in range(1, m + 1):
                if pc == "*":
                    dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
                elif pc == "?" or pc == s[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
        return dp[n][m]

    # dp over segments: match[i][j] = pat_segs[i:] matches path_segs[j:]
    P = len(pat_segs)
    S = len(path_segs)
    match = [[False] * (S + 1) for _ in range(P + 1)]
    match[P][S] = True
    for i in range(P - 1, -1, -1):
        ps = pat_segs[i]
        for j in range(S, -1, -1):
            if ps == "**":
                # zero segments, or consume one more and stay on **
                res = match[i + 1][j]
                if not res and j < S:
                    res = match[i][j + 1]
                match[i][j] = res
            else:
                if j < S and seg_match(ps, path_segs[j]):
                    match[i][j] = match[i + 1][j + 1]
                else:
                    match[i][j] = False
    return match[0][0]
