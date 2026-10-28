def glob_match(pattern: str, path: str) -> bool:
    pat_segs = pattern.split("/")
    path_segs = path.split("/")

    def seg_match(p: str, s: str) -> bool:
        # Match a single segment with ? and * (no "/" present in either).
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

    # Iterative matching over segments with "**" as a wildcard over whole segments.
    memo = {}

    def go(i: int, j: int) -> bool:
        key = (i, j)
        if key in memo:
            return memo[key]
        if i == len(pat_segs):
            res = j == len(path_segs)
        elif pat_segs[i] == "**":
            res = go(i + 1, j) or (j < len(path_segs) and go(i, j + 1))
        else:
            res = (
                j < len(path_segs)
                and seg_match(pat_segs[i], path_segs[j])
                and go(i + 1, j + 1)
            )
        memo[key] = res
        return res

    return go(0, 0)
