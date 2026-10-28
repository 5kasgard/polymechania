# NOTE: segment-level matching is linear-time per pair with backtracking on "*" only; the segment DP is O(len(pattern_segments) * len(path_segments)).

def _split(s: str) -> list:
    return [] if s == "" else s.split("/")


def _seg_match(p: str, s: str) -> bool:
    # Match one segment: "?" matches one character, "*" matches any run (possibly empty).
    i = j = 0
    star = -1
    mark = 0
    n, m = len(p), len(s)
    while j < m:
        if i < n and p[i] == "*":
            star = i
            mark = j
            i += 1
        elif i < n and (p[i] == "?" or p[i] == s[j]):
            i += 1
            j += 1
        elif star != -1:
            i = star + 1
            mark += 1
            j = mark
        else:
            return False
    while i < n and p[i] == "*":
        i += 1
    return i == n


def glob_match(pattern: str, path: str) -> bool:
    P = _split(pattern)
    S = _split(path)
    n = len(P)
    m = len(S)

    # nxt[j] == True iff P[i+1:] matches S[j:]
    # Start with i == n: matches only when no path segments remain.
    nxt = [j == m for j in range(m + 1)]

    for i in range(n - 1, -1, -1):
        cur = [False] * (m + 1)
        if P[i] == "**":
            # "**" matches zero segments (nxt[j]) or one more segment and stays on "**" (cur[j+1]).
            cur[m] = nxt[m]
            for j in range(m - 1, -1, -1):
                cur[j] = nxt[j] or cur[j + 1]
        else:
            cur[m] = False
            for j in range(m - 1, -1, -1):
                cur[j] = _seg_match(P[i], S[j]) and nxt[j + 1]
        nxt = cur

    return nxt[0]
