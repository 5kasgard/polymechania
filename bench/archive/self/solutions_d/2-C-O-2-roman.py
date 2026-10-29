_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

_CANON = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def _int_to_roman(n: int) -> str:
    parts = []
    for value, symbol in _CANON:
        count, n = divmod(n, value)
        parts.append(symbol * count)
    return "".join(parts)


def roman_to_int(s: str) -> int:
    if not isinstance(s, str) or not s:
        raise ValueError("empty or non-string Roman numeral")
    for ch in s:
        if ch not in _VALUES:
            raise ValueError(f"invalid Roman numeral character: {ch!r}")

    total = 0
    i = 0
    n = len(s)
    while i < n:
        v = _VALUES[s[i]]
        if i + 1 < n and _VALUES[s[i + 1]] > v:
            # Only the subtractive pairs IV IX XL XC CD CM are permitted.
            nxt = _VALUES[s[i + 1]]
            if nxt not in (5 * v, 10 * v):
                raise ValueError(f"invalid subtractive pair: {s[i:i+2]!r}")
            total += nxt - v
            i += 2
        else:
            total += v
            i += 1

    if not 1 <= total <= 3999:
        raise ValueError(f"value out of range 1..3999: {total}")
    if _int_to_roman(total) != s:
        raise ValueError(f"non-canonical Roman numeral: {s!r}")
    return total
