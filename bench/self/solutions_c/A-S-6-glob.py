from functools import lru_cache


def _segment_match(pat: str, seg: str) -> bool:
    # Iterative dynamic programming over the two strings; '*' stays within a segment.
    n, m = len(pat), len(seg)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(1, n + 1):
        if pat[i - 1] == "*":
            dp[i][0] = dp[i - 1][0]
    for i in range(1, n + 1):
        pc = pat[i - 1]
        for j in range(1, m + 1):
            if pc == "*":
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif pc == "?" or pc == seg[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[n][m]


def glob_match(pattern: str, path: str) -> bool:
    pat_segs = tuple(pattern.split("/"))
    path_segs = () if path == "" else tuple(path.split("/"))

    @lru_cache(maxsize=None)
    def go(pi: int, si: int) -> bool:
        if pi == len(pat_segs):
            return si == len(path_segs)
        p = pat_segs[pi]
        if p == "**":
            if go(pi + 1, si):
                return True
            return si < len(path_segs) and go(pi, si + 1)
        if si == len(path_segs):
            return False
        if not _segment_match(p, path_segs[si]):
            return False
        return go(pi + 1, si + 1)

    return go(0, 0)
