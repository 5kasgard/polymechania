from functools import lru_cache


def glob_match(pattern: str, path: str) -> bool:
    pat_segs = pattern.split("/")
    path_segs = [] if path == "" else path.split("/")
    n = len(pat_segs)
    m = len(path_segs)

    def seg_match(p: str, s: str) -> bool:
        # Match one non-"**" pattern segment against one path segment.
        # Iterative two-pointer approach with backtracking on "*".
        pi = si = 0
        star_p = -1
        star_s = 0
        lp, ls = len(p), len(s)
        while si < ls:
            if pi < lp and (p[pi] == "?" or (p[pi] != "*" and p[pi] == s[si])):
                pi += 1
                si += 1
            elif pi < lp and p[pi] == "*":
                star_p = pi
                star_s = si
                pi += 1
            elif star_p != -1:
                pi = star_p + 1
                star_s += 1
                si = star_s
            else:
                return False
        while pi < lp and p[pi] == "*":
            pi += 1
        return pi == lp

    # Iterative DP: reach[i][j] is True if pattern segments [i:] match path segments [j:].
    reach = [[False] * (m + 1) for _ in range(n + 1)]
    reach[n][m] = True
    for i in range(n - 1, -1, -1):
        p = pat_segs[i]
        for j in range(m, -1, -1):
            if p == "**":
                # Zero segments consumed, or absorb one more path segment.
                ok = reach[i + 1][j]
                if not ok and j < m:
                    ok = reach[i][j + 1]
                reach[i][j] = ok
            else:
                if j < m and seg_match(p, path_segs[j]):
                    reach[i][j] = reach[i + 1][j + 1]
                else:
                    reach[i][j] = False
    return reach[0][0]
