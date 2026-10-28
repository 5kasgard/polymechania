def roman_to_int(s: str) -> int:
    if not isinstance(s, str) or not s:
        raise ValueError("empty or non-string input")

    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    for ch in s:
        if ch not in values:
            raise ValueError(f"invalid character: {ch!r}")

    total = 0
    n = len(s)
    for i in range(n):
        v = values[s[i]]
        if i + 1 < n and v < values[s[i + 1]]:
            total -= v
        else:
            total += v

    if not (1 <= total <= 3999):
        raise ValueError("value out of range")

    if int_to_roman(total) != s:
        raise ValueError("not a canonical Roman numeral")
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
