def glob_match(pattern: str, path: str) -> bool:
    pat = pattern.split("/") if pattern != "" else []
    segs = path.split("/") if path != "" else []

    def seg_match(p: str, s: str) -> bool:
        # Match a single segment (no "/" inside either) with ? and *.
        # Iterative two-pointer matching with backtracking on '*'.
        i = j = 0
        star_i = -1
        star_j = -1
        n, m = len(p), len(s)
        while j < m:
            if i < n and p[i] == "?":
                i += 1
                j += 1
            elif i < n and p[i] == "*":
                star_i = i
                star_j = j
                i += 1
            elif i < n and p[i] == s[j]:
                i += 1
                j += 1
            elif star_i != -1:
                i = star_i + 1
                star_j += 1
                j = star_j
            else:
                return False
        while i < n and p[i] == "*":
            i += 1
        return i == n

    # Match pattern segments against path segments; "**" consumes zero or more segments.
    # Memoized DP over (pattern index, segment index) to avoid exponential blowup.
    P = len(pat)
    S = len(segs)
    memo = {}

    def go(pi: int, si: int) -> bool:
        key = (pi, si)
        if key in memo:
            return memo[key]
        if pi == P:
            res = si == S
        elif pat[pi] == "**":
            res = go(pi + 1, si) or (si < S and go(pi, si + 1))
        else:
            res = si < S and seg_match(pat[pi], segs[si]) and go(pi + 1, si + 1)
        memo[key] = res
        return res

    return go(0, 0)
