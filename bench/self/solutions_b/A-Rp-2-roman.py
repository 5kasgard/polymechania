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

    # Check for invalid characters or lowercase
    if any(c not in mapping for c in s):
        raise ValueError("Invalid characters in Roman numeral.")

    # Convert to values
    values = [mapping[c] for c in s]
    
    # Calculate integer value
    total = 0
    for i in range(len(values)):
        if i + 1 < len(values) and values[i] < values[i+1]:
            total += values[i+1] - values[i]
            # Skip the next element as it was part of a pair
            # We handle this by checking the logic in the canonical check
        else:
            total += values[i]

    # Re-calculate total correctly for subtraction logic
    total = 0
    i = 0
    while i < len(values):
        if i + 1 < len(values) and values[i] < values[i+1]:
            total += values[i+1] - values[i]
            i += 2
        else:
            total += values[i]
            i += 1

    # Canonical check: Convert the calculated integer back to Roman
    # and compare with the input string.
    def int_to_roman(n: int) -> str:
        if not (1 <= n <= 3999):
            return ""
        res = []
        # Standard subtractive pairs in descending order
        pairs = [
            (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
            (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
            (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
        ]
        for val, sym in pairs:
            while n >= val:
                res.append(sym)
                n -= val
        return "".join(res)

    if total < 1 or total > 3999 or int_to_roman(total) != s:
        raise ValueError("String is not in the unique canonical Roman numeral form.")

    return total
