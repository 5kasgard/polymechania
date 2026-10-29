from functools import lru_cache


def _seg_match(pat: str, seg: str) -> bool:
    # Match a single segment (no "/" inside) against a pattern segment
    # containing "?" and "*" wildcards. "*" matches any run of non-"/" chars,
    # which within a segment is any run of characters.
    n, m = len(pat), len(seg)
    # dp over pattern positions
    dp = [False] * (m + 1)
    dp[0] = True
    for pc in pat:
        ndp = [False] * (m + 1)
        if pc == "*":
            reach = False
            for j in range(m + 1):
                reach = reach or dp[j]
                ndp[j] = reach
        else:
            for j in range(1, m + 1):
                if dp[j - 1] and (pc == "?" or pc == seg[j - 1]):
                    ndp[j] = True
        dp = ndp
    return dp[m]


def glob_match(pattern: str, path: str) -> bool:
    pats = pattern.split("/")
    segs = path.split("/")
    if path == "":
        segs = []
    if pattern == "":
        pats = []

    np_, ns = len(pats), len(segs)

    @lru_cache(maxsize=None)
    def go(i: int, j: int) -> bool:
        if i == np_:
            return j == ns
        if pats[i] == "**":
            # zero segments, or consume one segment and stay on "**"
            if go(i + 1, j):
                return True
            return j < ns and go(i, j + 1)
        if j == ns:
            return False
        if not _seg_match(pats[i], segs[j]):
            return False
        return go(i + 1, j + 1)

    return go(0, 0)
