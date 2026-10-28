def _seg_match(pat: str, seg: str) -> bool:
    # Match a single segment: '?' matches one char, '*' matches any run (possibly empty).
    # Iterative two-pointer wildcard match with backtracking to the last '*'.
    p = s = 0
    star_p = -1
    star_s = 0
    n, m = len(pat), len(seg)
    while s < m:
        if p < n and (pat[p] == '?' or pat[p] == seg[s]):
            p += 1
            s += 1
        elif p < n and pat[p] == '*':
            star_p = p
            star_s = s
            p += 1
        elif star_p != -1:
            p = star_p + 1
            star_s += 1
            s = star_s
        else:
            return False
    while p < n and pat[p] == '*':
        p += 1
    return p == n


def glob_match(pattern: str, path: str) -> bool:
    pats = pattern.split('/') if pattern != '' else []
    segs = path.split('/') if path != '' else []
    # Note: "" yields no segments, "**" alone matches "" via zero segments.
    np, ns = len(pats), len(segs)

    # memo over (i, j): can pats[i:] match segs[j:]
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def go(i: int, j: int) -> bool:
        if i == np:
            return j == ns
        if pats[i] == '**':
            # zero segments, or consume one segment and stay on '**'
            if go(i + 1, j):
                return True
            return j < ns and go(i, j + 1)
        if j == ns:
            return False
        if _seg_match(pats[i], segs[j]):
            return go(i + 1, j + 1)
        return False

    return go(0, 0)
