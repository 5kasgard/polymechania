from functools import lru_cache


def _segment_match(pat: str, seg: str) -> bool:
    # Match one pattern segment (no "/") against one path segment (no "/").
    # "*" matches any run of characters, "?" matches exactly one character.
    p_len, s_len = len(pat), len(seg)
    # dp[j] = pattern prefix of length i matches seg prefix of length j
    dp = [False] * (s_len + 1)
    dp[0] = True
    for i in range(p_len):
        c = pat[i]
        new = [False] * (s_len + 1)
        if c == "*":
            # "*" can match empty (keep dp) or extend any previous match
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
    pat_segs = pattern.split("/")
    path_segs = path.split("/")
    n, m = len(pat_segs), len(path_segs)

    # Iterative DP over (pattern segment index i, path segment index j).
    # reach[i] is the set of path indices j such that pat_segs[:i] matches path_segs[:j].
    reach = [set() for _ in range(n + 1)]
    reach[0].add(0)
    for i in range(n):
        ps = pat_segs[i]
        if ps == "**":
            # Zero or more whole segments: propagate forward from every reachable j.
            if reach[i]:
                start = min(reach[i])
                reach[i + 1].update(range(start, m + 1))
                # Keep only states reachable under "**" semantics from each j.
                reach[i + 1] = set(range(start, m + 1))
        else:
            for j in reach[i]:
                if j < m and _segment_match(ps, path_segs[j]):
                    reach[i + 1].add(j + 1)
    return m in reach[n]
