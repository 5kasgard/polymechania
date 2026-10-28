from collections import Counter


def min_window(s: str, t: str) -> str:
    if not t or not s or len(t) > len(s):
        return ""
    need = Counter(t)
    missing = len(t)
    best_len = len(s) + 1
    best_start = 0
    left = 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            length = right - left + 1
            if length < best_len:
                best_len = length
                best_start = left
            need[s[left]] += 1
            missing += 1
            left += 1
    if best_len > len(s):
        return ""
    return s[best_start:best_start + best_len]
