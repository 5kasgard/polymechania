def multiply(a: str, b: str) -> str:
    if a == "0" or b == "0":
        return "0"

    sign = 1
    if a.startswith("-"):
        sign *= -1
        a = a[1:]
    if b.startswith("-"):
        sign *= -1
        b = b[1:]

    # Convert strings to lists of integers for digit-by-digit processing
    digits_a = [int(d) for d in a]
    digits_b = [int(d) for d in b]
    
    # Result array will have at most len(a) + len(b) digits
    res = [0] * (len(digits_a) + len(digits_b))

    # Standard long multiplication algorithm
    for i in range(len(digits_a) - 1, -1, -1):
        for j in range(len(digits_b) - 1, -1, -1):
            mul = digits_a[i] * digits_b[j]
            p1 = i + j
            p2 = i + j + 1
            
            total = mul + res[p2]
            res[p2] = total % 10
            res[p1] += total // 10

    # Convert result list back to string
    # Find the first non-zero digit
    start = 0
    while start < len(res) and res[start] == 0:
        start += 1
    
    if start == len(res):
        return "0"
    
    result_str = "".join(map(str, res[start:]))
    
    if sign == -1:
        return "-" + result_str
    return result_str
