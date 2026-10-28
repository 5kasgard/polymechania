def multiply(a: str, b: str) -> str:
    neg = (a[0] == "-") != (b[0] == "-")
    da = a.lstrip("-")
    db = b.lstrip("-")

    n, m = len(da), len(db)
    res = [0] * (n + m)
    for i in range(n - 1, -1, -1):
        x = ord(da[i]) - 48
        if x == 0:
            continue
        for j in range(m - 1, -1, -1):
            res[i + j + 1] += x * (ord(db[j]) - 48)

    carry = 0
    for k in range(n + m - 1, -1, -1):
        total = res[k] + carry
        res[k] = total % 10
        carry = total // 10

    idx = 0
    while idx < n + m - 1 and res[idx] == 0:
        idx += 1
    digits = "".join(chr(48 + d) for d in res[idx:])

    if digits == "0":
        return "0"
    return ("-" + digits) if neg else digits
