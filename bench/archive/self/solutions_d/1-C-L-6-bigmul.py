def multiply(a: str, b: str) -> str:
    # Sign handling: product is negative iff exactly one operand is negative.
    neg = (a[0] == "-") != (b[0] == "-")
    da = a[1:] if a[0] == "-" else a
    db = b[1:] if b[0] == "-" else b

    # Zero short-circuit keeps the result canonical ("0", never "-0").
    if da == "0" or db == "0":
        return "0"

    # Schoolbook digit-by-digit multiplication into a fixed-size buffer.
    # Digits are stored least-significant first; position i+j receives
    # the product of digit i of da and digit j of db. Accumulating raw
    # products in a list and carrying once at the end keeps the work at
    # O(len(da) * len(db)) with no int() conversion of the whole strings.
    la, lb = len(da), len(db)
    res = [0] * (la + lb)
    for i in range(la - 1, -1, -1):
        di = ord(da[i]) - 48
        if di == 0:
            continue
        carry = 0
        for j in range(lb - 1, -1, -1):
            cur = res[i + j + 1] + di * (ord(db[j]) - 48) + carry
            res[i + j + 1] = cur % 10
            carry = cur // 10
        res[i] += carry

    # Propagate any remaining carries (the top cell may still exceed 9).
    for k in range(la + lb - 1, 0, -1):
        if res[k] >= 10:
            res[k - 1] += res[k] // 10
            res[k] %= 10

    # Strip leading zeros and build the output string.
    digits = "".join(map(str, res)).lstrip("0")
    if not digits:
        return "0"
    return ("-" if neg else "") + digits
