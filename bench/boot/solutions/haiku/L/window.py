from collections import Counter


def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need = Counter(t)
    required = len(need)
    window = {}
    formed = 0
    best_len = len(s) + 1
    best_start = 0
    left = 0
    for right, ch in enumerate(s):
        if ch in need:
            window[ch] = window.get(ch, 0) + 1
            if window[ch] == need[ch]:
                formed += 1
        while formed == required:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_start = left
            lch = s[left]
            if lch in need:
                if window[lch] == need[lch]:
                    formed -= 1
                window[lch] -= 1
            left += 1
    if best_len > len(s):
        return ""
    return s[best_start:best_start + best_len]
