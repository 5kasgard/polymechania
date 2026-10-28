def glob_match(pattern: str, path: str) -> bool:
    pat = pattern.split("/") if pattern != "" else []
    segs = path.split("/") if path != "" else []
    n, m = len(pat), len(segs)

    def seg_match(p: str, s: str) -> bool:
        # Match one pattern segment (no "**") against one path segment.
        # "?" matches one non-"/" character; "*" matches any run of non-"/".
        # Segments never contain "/", so this is a plain wildcard match.
        pl, sl = len(p), len(s)
        # dp[i][j]: p[:i] matches s[:j]
        prev = [False] * (sl + 1)
        prev[0] = True
        for i in range(1, pl + 1):
            cur = [False] * (sl + 1)
            c = p[i - 1]
            if c == "*":
                cur[0] = prev[0]
                for j in range(1, sl + 1):
                    cur[j] = prev[j] or cur[j - 1]
            else:
                for j in range(1, sl + 1):
                    if prev[j - 1] and (c == "?" or c == s[j - 1]):
                        cur[j] = True
            prev = cur
        return prev[sl]

    # reach[j]: pattern prefix consumed so far can match segs[:j]
    # Process pattern segments left to right as a set of reachable indices.
    reach = {0}
    for i in range(n):
        p = pat[i]
        nxt = set()
        if p == "**":
            # "**" absorbs zero or more whole segments.
            if reach:
                start = min(reach)
                nxt.update(range(start, m + 1))
        else:
            for j in reach:
                if j < m and seg_match(p, segs[j]):
                    nxt.add(j + 1)
        reach = nxt
        if not reach:
            return False
    return m in reach
