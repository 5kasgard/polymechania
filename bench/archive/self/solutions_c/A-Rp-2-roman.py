import re

_PATTERN = re.compile(
    r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
)

_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s: str) -> int:
    if not isinstance(s, str) or not s or _PATTERN.fullmatch(s) is None:
        raise ValueError(f"not a canonical Roman numeral: {s!r}")
    total = 0
    n = len(s)
    for i, ch in enumerate(s):
        value = _VALUES[ch]
        if i + 1 < n and value < _VALUES[s[i + 1]]:
            total -= value
        else:
            total += value
    if total < 1:
        raise ValueError(f"not a canonical Roman numeral: {s!r}")
    return total
