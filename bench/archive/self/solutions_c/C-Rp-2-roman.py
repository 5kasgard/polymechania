def roman_to_int(s: str) -> int:
    if not isinstance(s, str) or not s:
        raise ValueError("empty or non-string input")

    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    for ch in s:
        if ch not in values:
            raise ValueError(f"invalid character: {ch!r}")

    total = 0
    n = len(s)
    for i, ch in enumerate(s):
        v = values[ch]
        if i + 1 < n and v < values[s[i + 1]]:
            total -= v
        else:
            total += v

    # Canonical-form check: re-encode and compare, which rejects
    # non-canonical forms like IIII, VX, IC, XM, VV, IIV, CMC.
    if total < 1 or total > 3999:
        raise ValueError("value out of range 1..3999")
    if _int_to_roman(total) != s:
        raise ValueError(f"not a canonical Roman numeral: {s!r}")
    return total


def _int_to_roman(num: int) -> str:
    table = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    out = []
    for value, symbol in table:
        count, num = divmod(num, value)
        out.append(symbol * count)
    return "".join(out)
