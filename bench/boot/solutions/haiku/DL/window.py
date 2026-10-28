from collections import Counter


def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need = Counter(t)
    required = len(need)
    have = {}
    formed = 0
    best_len = len(s) + 1
    best_l = 0
    l = 0
    for r, ch in enumerate(s):
        if ch in need:
            have[ch] = have.get(ch, 0) + 1
            if have[ch] == need[ch]:
                formed += 1
        while formed == required:
            if r - l + 1 < best_len:
                best_len = r - l + 1
                best_l = l
            left = s[l]
            if left in need:
                have[left] -= 1
                if have[left] < need[left]:
                    formed -= 1
            l += 1
    if best_len > len(s):
        return ""
    return s[best_l:best_l + best_len]
