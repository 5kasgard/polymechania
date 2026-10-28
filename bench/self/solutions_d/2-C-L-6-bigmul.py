def multiply(a: str, b: str) -> str:
    # Sign handling: product is negative when exactly one operand is negative.
    neg = (a[0] == "-") != (b[0] == "-")
    da = a.lstrip("-")
    db = b.lstrip("-")

    # Zero short-circuit keeps the result canonical ("0", never "-0").
    if da == "0" or db == "0":
        return "0"

    # Schoolbook multiplication on digit lists in base 10, accumulating
    # partial products into a single array indexed by place value.
    la, lb = len(da), len(db)
    res = [0] * (la + lb)
    for i in range(la - 1, -1, -1):
        x = ord(da[i]) - 48
        carry = 0
        for j in range(lb - 1, -1, -1):
            cur = res[i + j + 1] + x * (ord(db[j]) - 48) + carry
            res[i + j + 1] = cur % 10
            carry = cur // 10
        res[i] += carry

    # Strip leading zeros produced by the fixed-size buffer.
    start = 0
    while start < len(res) - 1 and res[start] == 0:
        start += 1
    digits = "".join(chr(d + 48) for d in res[start:])
    return "-" + digits if neg else digits
