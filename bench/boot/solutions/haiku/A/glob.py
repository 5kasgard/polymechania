def _segment_match(p: str, s: str) -> bool:
    # Match one path segment against one pattern segment (no "/" inside either).
    # "*" matches any run (possibly empty), "?" matches one character.
    i = j = 0
    star = -1
    mark = 0
    while j < len(s):
        if i < len(p) and p[i] == '*':
            star = i
            mark = j
            i += 1
        elif i < len(p) and (p[i] == '?' or p[i] == s[j]):
            i += 1
            j += 1
        elif star != -1:
            i = star + 1
            mark += 1
            j = mark
        else:
            return False
    while i < len(p) and p[i] == '*':
        i += 1
    return i == len(p)


def glob_match(pattern: str, path: str) -> bool:
    pat = pattern.split("/") if pattern else []
    segs = path.split("/") if path else []

    pi = 0
    si = 0
    star_p = -1
    star_s = 0
    while si < len(segs):
        if pi < len(pat) and pat[pi] == "**":
            star_p = pi
            star_s = si
            pi += 1
        elif pi < len(pat) and _segment_match(pat[pi], segs[si]):
            pi += 1
            si += 1
        elif star_p != -1:
            pi = star_p + 1
            star_s += 1
            si = star_s
        else:
            return False

    while pi < len(pat) and pat[pi] == "**":
        pi += 1
    return pi == len(pat)
