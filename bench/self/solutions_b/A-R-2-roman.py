def roman_to_int(s: str) -> int:
    """Converts a standard Roman numeral string to an integer."""
    mapping = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    if not s:
        raise ValueError("Empty string is not a valid Roman numeral.")

    # Validate characters and build integer value
    values = []
    for char in s:
        if char not in mapping:
            raise ValueError(f"Invalid character: {char}")
        values.append(mapping[char])

    # Calculate value using standard subtraction rule
    total = 0
    for i in range(len(values)):
        if i + 1 < len(values) and values[i] < values[i+1]:
            total += values[i+1] - values[i]
            # Skip the next element as it was part of the pair
            # We handle this by checking the next index in the loop logic
            # but to ensure we don't double count, we must adjust the loop.
            # Actually, a simpler way to validate canonical form is to 
            # convert the integer back to Roman and compare.
        else:
            total += values[i]

    # Re-calculating total correctly for subtraction pairs
    total = 0
    i = 0
    while i < len(values):
        if i + 1 < len(values) and values[i] < values[i+1]:
            total += values[i+1] - values[i]
            i += 2
        else:
            total += values[i]
            i += 1

    if not (1 <= total <= 3999):
        raise ValueError("Value out of range (1-3999).")

    # Canonical check: Convert total back to Roman and compare
    # This ensures "IIII", "VX", "IC", "MMMM", "iv", "XM", "VV", "IIV", "CMC" fail.
    def int_to_roman(n: int) -> str:
        val = [
            (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
            (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
            (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
        ]
        roman = ""
        for v, r in val:
            while n >= v:
                roman += r
                n -= v
        return roman

    if int_to_roman(total) != s:
        raise ValueError("String is not in the unique canonical Roman form.")

    return total
