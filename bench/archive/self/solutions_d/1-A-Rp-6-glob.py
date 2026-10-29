from functools import lru_cache


def _seg_match(pat: str, seg: str) -> bool:
    # Match one pattern segment (no "**") against one path segment.
    # "*" matches any run (possibly empty) within the segment; "?" one char.
    # Neither can cross "/" because segments contain no "/".
    p_len, s_len = len(pat), len(seg)
    # dp[j] = pat[:i] matches seg[:j]
    dp = [False] * (s_len + 1)
    dp[0] = True
    for i in range(p_len):
        c = pat[i]
        new = [False] * (s_len + 1)
        if c == "*":
            # "*" matches empty, or extends any prefix match by one char
            seen = False
            for j in range(s_len + 1):
                seen = seen or dp[j]
                new[j] = seen
        else:
            for j in range(1, s_len + 1):
                if dp[j - 1] and (c == "?" or c == seg[j - 1]):
                    new[j] = True
        dp = new
    return dp[s_len]


def glob_match(pattern: str, path: str) -> bool:
    pat_segs = tuple(pattern.split("/"))
    path_segs = tuple(path.split("/"))
    n_pat = len(pat_segs)
    n_path = len(path_segs)

    @lru_cache(maxsize=None)
    def go(i: int, j: int) -> bool:
        # Can pat_segs[i:] match path_segs[j:]?
        if i == n_pat:
            return j == n_path
        if pat_segs[i] == "**":
            # Absorb zero or more whole segments.
            if go(i + 1, j):
                return True
            return j < n_path and go(i, j + 1)
        if j == n_path:
            return False
        if not _seg_match(pat_segs[i], path_segs[j]):
            return False
        return go(i + 1, j + 1)

    return go(0, 0)
