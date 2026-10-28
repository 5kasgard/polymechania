import fnmatch  # noqa: F401  (standard library only; not used)


def _match_segment(pat: str, seg: str) -> bool:
    # Match a single segment (no "/" inside either string).
    # "?" matches exactly one character, "*" matches any run (possibly empty).
    # Iterative two-pointer matcher with backtracking to the last "*".
    pi = si = 0
    star_pi = -1
    star_si = 0
    np, ns = len(pat), len(seg)
    while si < ns:
        if pi < np and pat[pi] == "*":
            star_pi = pi
            star_si = si
            pi += 1
        elif pi < np and (pat[pi] == "?" or pat[pi] == seg[si]):
            pi += 1
            si += 1
        elif star_pi != -1:
            pi = star_pi + 1
            star_si += 1
            si = star_si
        else:
            return False
    while pi < np and pat[pi] == "*":
        pi += 1
    return pi == np


def _match_segments(pats, segs) -> bool:
    # Iterative DP over (pattern index, segment index) to avoid deep recursion.
    np, ns = len(pats), len(segs)
    # reach[j] = True if pats[:i] can match segs[:j]
    reach = [False] * (ns + 1)
    reach[0] = True
    for i in range(np):
        p = pats[i]
        new = [False] * (ns + 1)
        if p == "**":
            # zero or more whole segments: once reachable, stays reachable onward
            seen = False
            for j in range(ns + 1):
                seen = seen or reach[j]
                new[j] = seen
        else:
            for j in range(1, ns + 1):
                if reach[j - 1] and _match_segment(p, segs[j - 1]):
                    new[j] = True
        reach = new
    return reach[ns]


def glob_match(pattern: str, path: str) -> bool:
    pats = pattern.split("/")
    segs = path.split("/")
    if path == "":
        segs = []
    if pattern == "":
        pats = []
    return _match_segments(pats, segs)
