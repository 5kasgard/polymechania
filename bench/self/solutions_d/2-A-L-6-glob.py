from functools import lru_cache


def _segment_match(pat: str, seg: str) -> bool:
    # Match one segment, where '*' matches any run of non-'/' characters
    # and '?' matches exactly one character. Segments contain no '/'.
    n, m = len(pat), len(seg)
    # dp[j] = pat[:i] matches seg[:j]
    prev = [False] * (m + 1)
    prev[0] = True
    for i in range(n):
        c = pat[i]
        cur = [False] * (m + 1)
        if c == '*':
            cur[0] = prev[0]
            for j in range(1, m + 1):
                cur[j] = prev[j] or cur[j - 1]
        else:
            for j in range(1, m + 1):
                if prev[j - 1] and (c == '?' or c == seg[j - 1]):
                    cur[j] = True
        prev = cur
    return prev[m]


def glob_match(pattern: str, path: str) -> bool:
    pats = pattern.split('/')
    segs = path.split('/')
    np_, ns = len(pats), len(segs)

    @lru_cache(maxsize=None)
    def go(i: int, j: int) -> bool:
        # Match pats[i:] against segs[j:]
        if i == np_:
            return j == ns
        if pats[i] == '**':
            # '**' consumes zero or more whole segments
            if go(i + 1, j):
                return True
            return j < ns and go(i, j + 1)
        if j == ns:
            return False
        if not _segment_match(pats[i], segs[j]):
            return False
        return go(i + 1, j + 1)

    return go(0, 0)
