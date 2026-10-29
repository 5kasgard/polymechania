def roman_to_int(s: str) -> int:
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    if not isinstance(s, str) or not s:
        raise ValueError("invalid roman numeral")
    for ch in s:
        if ch not in values:
            raise ValueError("invalid roman numeral")

    total = 0
    n = len(s)
    i = 0
    while i < n:
        cur = values[s[i]]
        if i + 1 < n and values[s[i + 1]] > cur:
            nxt = values[s[i + 1]]
            # Only subtractive pairs IV IX XL XC CD CM are allowed.
            if nxt not in (5 * cur, 10 * cur):
                raise ValueError("invalid roman numeral")
            total += nxt - cur
            i += 2
        else:
            total += cur
            i += 1

    if total < 1 or total > 3999:
        raise ValueError("invalid roman numeral")

    # Canonical check: re-encode and compare, so forms like IIII, VV, IIV,
    # VX, XM, CMC and similar non-canonical strings are rejected.
    if _int_to_roman(total) != s:
        raise ValueError("invalid roman numeral")
    return total


def _int_to_roman(num: int) -> str:
    pairs = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    out = []
    for value, sym in pairs:
        while num >= value:
            out.append(sym)
            num -= value
    return "".join(out)
