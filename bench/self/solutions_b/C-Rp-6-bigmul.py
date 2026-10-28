def multiply(a: str, b: str) -> str:
    if a == "0" or b == "0":
        return "0"

    # Handle signs
    is_negative = False
    if a.startswith("-"):
        is_negative = not is_negative
        a = a[1:]
    if b.startswith("-"):
        is_negative = not is_negative
        b = b[1:]

    # Convert strings to lists of integers (digits)
    # We reverse them so that index i corresponds to 10^i
    digits_a = [int(d) for d in reversed(a)]
    digits_b = [int(d) for d in reversed(b)]
    
    # The product of an n-digit and m-digit number has at most n+m digits
    res = [0] * (len(digits_a) + len(digits_b))

    # Grade-school multiplication
    for i in range(len(digits_a)):
        for j in range(len(digits_b)):
            res[i + j] += digits_a[i] * digits_b[j]
            # Handle carry immediately to keep numbers in res small
            if res[i + j] >= 10:
                res[i + j + 1] += res[i + j] // 10
                res[i + j] %= 10

    # Remove trailing zeros (which are leading zeros in the final number)
    while len(res) > 1 and res[-1] == 0:
        res.pop()

    # Convert back to string
    result_str = "".join(str(d) for d in reversed(res))
    
    if is_negative and result_str != "0":
        return "-" + result_str
    return result_str
