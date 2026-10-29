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
            v2 = values[s[i + 1]]
            # only subtractive pairs IV IX XL XC CD CM are allowed
            if v2 // v not in (5, 10) or s[i:i + 2] not in ("IV", "IX", "XL", "XC", "CD", "CM"):
                raise ValueError("invalid Roman numeral")
            total += v2 - v
            i += 2
        else:
            total += v
            i += 1

    if not 1 <= total <= 3999:
        raise ValueError("invalid Roman numeral")

    # canonical check: the only valid form of total must be s
    if int_to_roman(total) != s:
        raise ValueError("invalid Roman numeral")
    return total


def int_to_roman(n: int) -> str:
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
