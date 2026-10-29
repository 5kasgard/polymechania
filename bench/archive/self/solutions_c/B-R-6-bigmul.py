def multiply(a: str, b: str) -> str:
    neg = (a[0] == "-") != (b[0] == "-")
    da = a.lstrip("-")
    db = b.lstrip("-")
    if da == "0" or db == "0":
        return "0"
    na, nb = len(da), len(db)
    res = [0] * (na + nb)
    for i in range(na - 1, -1, -1):
        x = ord(da[i]) - 48
        carry = 0
        for j in range(nb - 1, -1, -1):
            y = ord(db[j]) - 48
            cur = res[i + j + 1] + x * y + carry
            res[i + j + 1] = cur % 10
            carry = cur // 10
        res[i] += carry
    start = 0
    while start < len(res) - 1 and res[start] == 0:
        start += 1
    digits = "".join(chr(48 + d) for d in res[start:])
    return "-" + digits if neg else digits
