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

    # Only the canonical form is accepted: re-encode and compare.
    if total < 1 or total > 3999:
        raise ValueError("value out of range 1..3999")

    digits = [
        ("M", 1000), ("CM", 900), ("D", 500), ("CD", 400),
        ("C", 100), ("XC", 90), ("L", 50), ("XL", 40),
        ("X", 10), ("IX", 9), ("V", 5), ("IV", 4), ("I", 1),
    ]
    out = []
    rem = total
    for sym, val in digits:
        while rem >= val:
            out.append(sym)
            rem -= val
    if "".join(out) != s:
        raise ValueError("not a canonical Roman numeral")

    return total
