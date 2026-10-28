def multiply(a: str, b: str) -> str:
    if a == "0" or b == "0":
        return "0"

    # Determine sign
    is_negative = False
    if a.startswith("-"):
        is_negative = not is_negative
        a = a[1:]
    if b.startswith("-"):
        is_negative = not is_negative
        b = b[1:]

    # Validate and convert to digit lists
    def to_digits(s: str) -> list[int]:
        if not s:
            raise ValueError("Empty input")
        if len(s) > 1 and s[0] == '0':
            raise ValueError("Leading zeros not allowed")
        digits = []
        for char in s:
            if not ('0' <= char <= '9'):
                raise ValueError("Invalid digit")
            digits.append(ord(char) - ord('0'))
        return digits

    digits_a = to_digits(a)
    digits_b = to_digits(b)

    # Long multiplication
    # Result can have at most len(a) + len(b) digits
    res_len = len(digits_a) + len(digits_b)
    res = [0] * res_len

    # Multiply digit by digit
    for i in range(len(digits_a) - 1, -1, -1):
        for j in range(len(digits_b) - 1, -1, -1):
            mul = digits_a[i] * digits_b[j]
            # The position in the result array
            pos_low = i + j + 1
            pos_high = i + j
            
            total = mul + res[pos_low]
            res[pos_low] = total % 10
            res[pos_high] += total // 10

    # Convert result array to string
    # Find the first non-zero digit
    start_idx = 0
    while start_idx < len(res) and res[start_idx] == 0:
        start_idx += 1
    
    if start_idx == len(res):
        return "0"

    result_str = "".join(str(d) for d in res[start_idx:])
    
    if is_negative:
        return "-" + result_str
    return result_str
