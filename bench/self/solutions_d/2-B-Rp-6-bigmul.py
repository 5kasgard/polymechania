def multiply(a: str, b: str) -> str:
    neg = (a[0] == "-") != (b[0] == "-")
    da = a.lstrip("-")
    db = b.lstrip("-")
    if da == "0" or db == "0":
        return "0"

    la, lb = len(da), len(db)
    acc = [0] * (la + lb)
    for i in range(la - 1, -1, -1):
        x = ord(da[i]) - 48
        if x == 0:
            continue
        for j in range(lb - 1, -1, -1):
            acc[i + j + 1] += x * (ord(db[j]) - 48)

    carry = 0
    for k in range(la + lb - 1, -1, -1):
        total = acc[k] + carry
        acc[k] = total % 10
        carry = total // 10

    digits = "".join(map(str, acc)).lstrip("0")
    if not digits:
        return "0"
    return "-" + digits if neg else digits
