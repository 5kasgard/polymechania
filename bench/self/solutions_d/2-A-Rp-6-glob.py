from functools import lru_cache


def _segment_match(pat: str, seg: str) -> bool:
    # Dynamic programming over characters; "*" matches any run, "?" one char.
    n, m = len(pat), len(seg)
    prev = [False] * (m + 1)
    prev[0] = True
    for i in range(n):
        cur = [False] * (m + 1)
        c = pat[i]
        if c == "*":
            cur[0] = prev[0]
            for j in range(1, m + 1):
                cur[j] = cur[j - 1] or prev[j]
        else:
            for j in range(1, m + 1):
                if prev[j - 1] and (c == "?" or c == seg[j - 1]):
                    cur[j] = True
        prev = cur
    return prev[m]


def glob_match(pattern: str, path: str) -> bool:
    pats = pattern.split("/") if pattern != "" else []
    segs = path.split("/") if path != "" else []
    # Note: "" has zero segments; "a//b" splits into ["a", "", "b"] as required.

    np_, ns = len(pats), len(segs)

    @lru_cache(maxsize=None)
    def go(i: int, j: int) -> bool:
        if i == np_:
            return j == ns
        p = pats[i]
        if p == "**":
            # Zero segments consumed, or consume one segment and stay on "**".
            if go(i + 1, j):
                return True
            return j < ns and go(i, j + 1)
        if j == ns:
            return False
        return _segment_match(p, segs[j]) and go(i + 1, j + 1)

    return go(0, 0)
