def multiply(a: str, b: str) -> str:
    # Sign handling: the product is negative exactly when one operand is negative
    # and the other is not. Work on the absolute digit strings.
    neg = (a[0] == "-") != (b[0] == "-")
    da = a.lstrip("-")
    db = b.lstrip("-")

    # Zero short-circuit keeps the result "0" and avoids a "-0" result.
    if da == "0" or db == "0":
        return "0"

    # Schoolbook multiplication on digit arrays. The product of an m-digit and
    # an n-digit number has at most m+n digits, so accumulate into that buffer.
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

    # Strip leading zeros from the buffer and convert back to a string.
    k = 0
    while k < len(res) - 1 and res[k] == 0:
        k += 1
    digits = "".join(chr(d + 48) for d in res[k:])
    return "-" + digits if neg else digits
