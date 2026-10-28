import re

_PATTERN = re.compile(r'^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')

_VALUES = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}


def roman_to_int(s: str) -> int:
    if not isinstance(s, str) or not s:
        raise ValueError("invalid Roman numeral")
    if not s.isascii() or not _PATTERN.fullmatch(s):
        raise ValueError("invalid Roman numeral")
    total = 0
    prev = 0
    for ch in reversed(s):
        v = _VALUES[ch]
        if v < prev:
            total -= v
        else:
            total += v
            prev = v
    if not 1 <= total <= 3999:
        raise ValueError("invalid Roman numeral")
    return total
