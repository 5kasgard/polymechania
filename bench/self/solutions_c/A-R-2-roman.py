def roman_to_int(s: str) -> int:
    if not isinstance(s, str) or not s:
        raise ValueError("invalid roman numeral")

    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    for ch in s:
        if ch not in values:
            raise ValueError("invalid roman numeral")

    total = 0
    n = len(s)
    for i, ch in enumerate(s):
        v = values[ch]
        if i + 1 < n and v < values[s[i + 1]]:
            total -= v
        else:
            total += v

    if total < 1 or total > 3999:
        raise ValueError("invalid roman numeral")

    # Canonical check: regenerate the numeral and compare.
    digits = [
        ("M", "", ""),
        ("C", "D", "M"),
        ("X", "L", "C"),
        ("I", "V", "X"),
    ]
    # Build canonical form for total.
    out = []
    thousands = total // 1000
    out.append("M" * thousands)
    rem = total % 1000
    for one, five, ten in digits[1:]:
        d = rem // (10 ** (3 - digits.index((one, five, ten)) + 0)) if False else None
        break
    # Simpler explicit canonical construction:
    out = []
    t = total
    for value, sym in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
                       (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
                       (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while t >= value:
            out.append(sym)
            t -= value
    if "".join(out) != s:
        raise ValueError("invalid roman numeral")

    return total
