_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def _int_to_roman(n: int) -> str:
    table = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    out = []
    for value, symbol in table:
        while n >= value:
            out.append(symbol)
            n -= value
    return "".join(out)


def roman_to_int(s: str) -> int:
    if not isinstance(s, str) or not s:
        raise ValueError("empty or non-string Roman numeral")

    total = 0
    for i, ch in enumerate(s):
        if ch not in _VALUES:
            raise ValueError(f"invalid character {ch!r}")
        value = _VALUES[ch]
        if i + 1 < len(s) and _VALUES[s[i + 1]] > value:
            total -= value
        else:
            total += value

    if not 1 <= total <= 3999:
        raise ValueError("value out of range 1..3999")
    if _int_to_roman(total) != s:
        raise ValueError("not a canonical Roman numeral")
    return total
