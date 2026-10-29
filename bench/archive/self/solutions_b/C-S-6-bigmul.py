def multiply(a: str, b: str) -> str:
    if a == "0" or b == "0":
        return "0"

    # Determine the sign of the result
    is_negative = False
    if a.startswith("-"):
        is_negative = not is_negative
        a = a[1:]
    if b.startswith("-"):
        is_negative = not is_negative
        b = b[1:]

    # Convert strings to lists of integers for digit-by-digit processing
    # We reverse them so that index i corresponds to the 10^i position
    digits_a = [int(d) for d in reversed(a)]
    digits_b = [int(d) for d in reversed(b)]

    # The maximum possible length of the product is len(a) + len(b)
    res_len = len(digits_a) + len(digits_b)
    result = [0] * res_len

    # Perform digit-by-digit multiplication
    for i in range(len(digits_a)):
        for j in range(len(digits_b)):
            # Multiply digits and add to the current position in the result array
            result[i + j] += digits_a[i] * digits_b[j]
            
            # Handle carry immediately to prevent very large numbers in a single cell,
            # though Python handles arbitrary size ints, it's cleaner.
            if result[i + j] >= 10:
                result[i + j + 1] += result[i + j] // 10
                result[i + j] %= 10

    # Convert the result list back to a string
    # Remove trailing zeros (which are leading zeros in the final number)
    while len(result) > 1 and result[-1] == 0:
        result.pop()

    # Join digits
    product_str = "".join(str(d) for d in reversed(result))

    # Handle the "0" case and sign
    if product_str == "0":
        return "0"
    
    return "-" + product_str if is_negative else product_str
