import re

_ROMAN_RE = re.compile(
    r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})"
)

_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def _int_to_roman(n: int) -> str:
    table = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    out = []
    for value, sym in table:
        while n >= value:
            out.append(sym)
            n -= value
    return "".join(out)


def roman_to_int(s: str) -> int:
    if not isinstance(s, str) or not s:
        raise ValueError("empty or non-string Roman numeral")
    if not _ROMAN_RE.fullmatch(s):
        raise ValueError(f"invalid Roman numeral: {s!r}")

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
        raise ValueError(f"value out of range 1..3999: {s!r}")
    if _int_to_roman(total) != s:
        raise ValueError(f"non-canonical Roman numeral: {s!r}")
    return total
