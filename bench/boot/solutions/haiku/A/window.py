from collections import Counter


def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need = Counter(t)
    missing = len(t)
    best_len = len(s) + 1
    best_l = 0
    l = 0
    for r, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:
            while need[s[l]] < 0:
                need[s[l]] += 1
                l += 1
            if r - l + 1 < best_len:
                best_len = r - l + 1
                best_l = l
            need[s[l]] += 1
            missing += 1
            l += 1
    if best_len > len(s):
        return ""
    return s[best_l:best_l + best_len]
