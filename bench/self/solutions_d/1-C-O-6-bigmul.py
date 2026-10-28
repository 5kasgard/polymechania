def multiply(a: str, b: str) -> str:
    neg = False
    if a.startswith("-"):
        neg = not neg
        a = a[1:]
    if b.startswith("-"):
        neg = not neg
        b = b[1:]

    la, lb = len(a), len(b)
    res = [0] * (la + lb)
    for i in range(la - 1, -1, -1):
        da = ord(a[i]) - 48
        if da == 0:
            continue
        for j in range(lb - 1, -1, -1):
            res[i + j + 1] += da * (ord(b[j]) - 48)

    carry = 0
    for k in range(la + lb - 1, -1, -1):
        total = res[k] + carry
        res[k] = total % 10
        carry = total // 10

    digits = "".join(map(str, res)).lstrip("0")
    if not digits:
        return "0"
    return ("-" + digits) if neg else digits
