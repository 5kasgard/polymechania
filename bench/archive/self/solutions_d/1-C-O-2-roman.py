def roman_to_int(s: str) -> int:
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    if not isinstance(s, str) or not s:
        raise ValueError("invalid Roman numeral")
    for ch in s:
        if ch not in values:
            raise ValueError("invalid Roman numeral")

    total = 0
    n = len(s)
    i = 0
    while i < n:
        v = values[s[i]]
        if i + 1 < n and values[s[i + 1]] > v:
            # subtractive pair: only IV IX XL XC CD CM are allowed
            w = values[s[i + 1]]
            if w not in (5 * v, 10 * v) or v not in (1, 10, 100):
                raise ValueError("invalid Roman numeral")
            total += w - v
            i += 2
        else:
            total += v
            i += 1

    if total < 1 or total > 3999:
        raise ValueError("invalid Roman numeral")

    # Reject any non-canonical spelling by round-tripping through the
    # canonical encoder.
    if _to_roman(total) != s:
        raise ValueError("invalid Roman numeral")
    return total


def _to_roman(num: int) -> str:
    table = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    out = []
    for value, sym in table:
        while num >= value:
            out.append(sym)
            num -= value
    return "".join(out)
