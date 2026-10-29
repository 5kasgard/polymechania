def glob_match(pattern: str, path: str) -> bool:
    pat_segs = pattern.split("/")
    path_segs = path.split("/")

    def seg_match(p: str, s: str) -> bool:
        # Iterative wildcard matching for one segment: '?' matches one char,
        # '*' matches any run (possibly empty). Neither crosses '/' since
        # segments contain no '/'.
        pi = si = 0
        star_pi = -1
        star_si = 0
        n, m = len(p), len(s)
        while si < m:
            if pi < n and (p[pi] == "?" or p[pi] == s[si]) and p[pi] != "*":
                pi += 1
                si += 1
            elif pi < n and p[pi] == "*":
                star_pi = pi
                star_si = si
                pi += 1
            elif star_pi != -1:
                pi = star_pi + 1
                star_si += 1
                si = star_si
            else:
                return False
        while pi < n and p[pi] == "*":
            pi += 1
        return pi == n

    # Memoised matching of pattern segments from index pi against path
    # segments from index si, where "**" consumes zero or more segments.
    from functools import lru_cache

    np_, ns_ = len(pat_segs), len(path_segs)

    @lru_cache(maxsize=None)
    def go(pi: int, si: int) -> bool:
        if pi == np_:
            return si == ns_
        p = pat_segs[pi]
        if p == "**":
            # Zero segments, or consume one path segment and stay on "**".
            if go(pi + 1, si):
                return True
            return si < ns_ and go(pi, si + 1)
        if si == ns_:
            return False
        return seg_match(p, path_segs[si]) and go(pi + 1, si + 1)

    return go(0, 0)
