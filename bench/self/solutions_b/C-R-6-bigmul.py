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
    
    n = len(digits_a)
    m = len(digits_b)
    result = [0] * (n + m)

    # Standard multiplication algorithm (O(N*M))
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            mul = digits_a[i] * digits_b[j]
            p1 = i + j
            p2 = i + j + 1
            total = mul + result[p2]

            result[p2] = total % 10
            result[p1] += total // 10

    # Convert result list back to string
    # Find the first non-zero digit
    start = 0
    while start < len(result) and result[start] == 0:
        start += 1
    
    if start == len(result):
        return "0"
    
    res_str = "".join(map(str, result[start:]))
    
    if sign == -1:
        return "-" + res_str
    return res_str
