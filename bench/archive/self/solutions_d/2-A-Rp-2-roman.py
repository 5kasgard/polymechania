import re

_PATTERN = re.compile(
    r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
)

_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s: str) -> int:
    if not isinstance(s, str) or not s or not _PATTERN.fullmatch(s):
        raise ValueError(f"not a canonical Roman numeral: {s!r}")
    total = 0
    n = len(s)
    for i, ch in enumerate(s):
        v = _VALUES[ch]
        if i + 1 < n and v < _VALUES[s[i + 1]]:
            total -= v
        else:
            total += v
    if total < 1 or total > 3999:
        raise ValueError(f"not a canonical Roman numeral: {s!r}")
    return total
