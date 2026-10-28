def glob_match(pattern: str, path: str) -> bool:
    pat_segs = pattern.split("/")
    path_segs = path.split("/")

    def seg_match(p: str, s: str) -> bool:
        # Match a single segment (no "/" inside either) with "?" and "*".
        # Iterative two-pointer matcher with backtracking to last star.
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

    # Memoised DP over (pattern segment index, path segment index).
    from functools import lru_cache

    np = len(pat_segs)
    ns = len(path_segs)

    @lru_cache(maxsize=None)
    def match_from(i: int, j: int) -> bool:
        if i == np:
            return j == ns
        if pat_segs[i] == "**":
            # "**" consumes zero or more whole segments.
            if match_from(i + 1, j):
                return True
            if j < ns and match_from(i, j + 1):
                return True
            return False
        if j == ns:
            return False
        if seg_match(pat_segs[i], path_segs[j]):
            return match_from(i + 1, j + 1)
        return False

    return match_from(0, 0)
