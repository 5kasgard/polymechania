def multiply(a: str, b: str) -> str:
    neg = (a[0] == "-") != (b[0] == "-")
    da = a[1:] if a[0] == "-" else a
    db = b[1:] if b[0] == "-" else b

    la, lb = len(da), len(db)
    res = [0] * (la + lb)

    for i in range(la - 1, -1, -1):
        x = ord(da[i]) - 48
        if x == 0:
            continue
        carry = 0
        for j in range(lb - 1, -1, -1):
            k = i + j + 1
            cur = res[k] + x * (ord(db[j]) - 48) + carry
            res[k] = cur % 10
            carry = cur // 10
        res[i] += carry

    start = 0
    while start < len(res) - 1 and res[start] == 0:
        start += 1
    digits = "".join(chr(48 + d) for d in res[start:])

    if digits == "0":
        return "0"
    return "-" + digits if neg else digits
