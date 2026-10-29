def roman_to_int(s: str) -> int:
    if not isinstance(s, str) or not s:
        raise ValueError("invalid roman numeral")

    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    for ch in s:
        if ch not in values:
            raise ValueError("invalid roman numeral")

    total = 0
    n = len(s)
    for i in range(n):
        v = values[s[i]]
        if i + 1 < n and v < values[s[i + 1]]:
            total -= v
        else:
            total += v

    if total < 1 or total > 3999:
        raise ValueError("invalid roman numeral")

    # Canonical check: re-encode and compare exactly.
    digits = [
        ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"),
    ][0]
    pairs = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    out = []
    rem = total
    for val, sym in pairs:
        while rem >= val:
            out.append(sym)
            rem -= val
    if "".join(out) != s:
        raise ValueError("invalid roman numeral")

    return total
