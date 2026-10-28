def glob_match(pattern: str, path: str) -> bool:
    pat_segs = pattern.split("/")
    path_segs = path.split("/")

    def seg_match(p: str, s: str) -> bool:
        # Match a single segment: "?" matches one char, "*" matches any run.
        # Iterative two-pointer matching with backtracking on the last "*".
        pi = si = 0
        star_pi = -1
        star_si = 0
        while si < len(s):
            if pi < len(p) and p[pi] == "*":
                star_pi = pi
                star_si = si
                pi += 1
            elif pi < len(p) and (p[pi] == "?" or p[pi] == s[si]):
                pi += 1
                si += 1
            elif star_pi != -1:
                pi = star_pi + 1
                star_si += 1
                si = star_si
            else:
                return False
        while pi < len(p) and p[pi] == "*":
            pi += 1
        return pi == len(p)

    # Match segment lists; "**" consumes zero or more whole segments.
    # Memoised DP over (pattern index, path index) to avoid exponential blowup.
    n, m = len(pat_segs), len(path_segs)
    memo = {}

    def go(i: int, j: int) -> bool:
        key = (i, j)
        if key in memo:
            return memo[key]
        if i == n:
            res = j == m
        elif pat_segs[i] == "**":
            # Zero segments, or consume one path segment and stay on "**".
            res = go(i + 1, j) or (j < m and go(i, j + 1))
        else:
            res = (
                j < m
                and seg_match(pat_segs[i], path_segs[j])
                and go(i + 1, j + 1)
            )
        memo[key] = res
        return res

    return go(0, 0)
