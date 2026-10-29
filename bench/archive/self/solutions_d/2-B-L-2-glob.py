def glob_match(pattern: str, path: str) -> bool:
    pat_segs = pattern.split("/")
    path_segs = path.split("/")

    def seg_match(p: str, s: str) -> bool:
        # Match a single segment: '?' matches one char, '*' matches any run.
        # Iterative two-pointer matching with backtracking to last '*'.
        pi = si = 0
        star_pi = -1
        star_si = 0
        n, m = len(p), len(s)
        while si < m:
            if pi < n and p[pi] == "*":
                star_pi = pi
                star_si = si
                pi += 1
            elif pi < n and (p[pi] == "?" or p[pi] == s[si]):
                pi += 1
                si += 1
            elif star_pi != -1:
                pi = star_pi + 1
                star_si += 1
                si = star_si
            else:
                return False
        while pi < n and p[pi] == "*":
            pi += 1
        return pi == n

    # Dynamic programming over (pattern segment index, path segment index),
    # where "**" consumes zero or more whole path segments.
    from functools import lru_cache

    P = len(pat_segs)
    S = len(path_segs)

    @lru_cache(maxsize=None)
    def go(i: int, j: int) -> bool:
        if i == P:
            return j == S
        if pat_segs[i] == "**":
            # Zero segments, or consume one path segment and stay on "**".
            if go(i + 1, j):
                return True
            return j < S and go(i, j + 1)
        if j == S:
            return False
        if not seg_match(pat_segs[i], path_segs[j]):
            return False
        return go(i + 1, j + 1)

    if path == "" and pattern == "":
        return True
    return go(0, 0)
