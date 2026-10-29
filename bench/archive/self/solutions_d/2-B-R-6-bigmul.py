def multiply(a: str, b: str) -> str:
    neg_a = a.startswith("-")
    neg_b = b.startswith("-")
    da = a[1:] if neg_a else a
    db = b[1:] if neg_b else b

    if da == "0" or db == "0":
        return "0"

    la, lb = len(da), len(db)
    res = [0] * (la + lb)
    for i in range(la - 1, -1, -1):
        x = ord(da[i]) - 48
        if x == 0:
            continue
        carry = 0
        for j in range(lb - 1, -1, -1):
            y = ord(db[j]) - 48
            cur = res[i + j + 1] + x * y + carry
            res[i + j + 1] = cur % 10
            carry = cur // 10
        res[i] += carry

    start = 0
    while start < len(res) - 1 and res[start] == 0:
        start += 1
    digits = "".join(chr(d + 48) for d in res[start:])

    if neg_a != neg_b:
        return "-" + digits
    return digits
