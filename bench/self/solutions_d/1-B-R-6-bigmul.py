def multiply(a: str, b: str) -> str:
    neg = (a[0] == "-") != (b[0] == "-")
    x = a.lstrip("-")
    y = b.lstrip("-")
    if x == "0" or y == "0":
        return "0"
    n, m = len(x), len(y)
    digits = [0] * (n + m)
    for i in range(n - 1, -1, -1):
        xi = ord(x[i]) - 48
        if xi == 0:
            continue
        carry = 0
        for j in range(m - 1, -1, -1):
            cur = digits[i + j + 1] + xi * (ord(y[j]) - 48) + carry
            digits[i + j + 1] = cur % 10
            carry = cur // 10
        digits[i] += carry
    start = 0
    while start < len(digits) - 1 and digits[start] == 0:
        start += 1
    result = "".join(chr(48 + d) for d in digits[start:])
    return "-" + result if neg else result
