def multiply(a: str, b: str) -> str:
    # Sign handling: negative if exactly one operand is negative.
    neg = a.startswith("-") != b.startswith("-")
    da = a.lstrip("-")
    db = b.lstrip("-")

    # Zero short-circuit: result is "0" (never "-0").
    if da == "0" or db == "0":
        return "0"

    # Work with reversed digit values so index i corresponds to 10**i.
    xa = [ord(c) - 48 for c in reversed(da)]
    xb = [ord(c) - 48 for c in reversed(db)]

    res = [0] * (len(xa) + len(xb))
    for i, x in enumerate(xa):
        if x == 0:
            continue
        carry = 0
        for j, y in enumerate(xb):
            cur = res[i + j] + x * y + carry
            res[i + j] = cur % 10
            carry = cur // 10
        k = i + len(xb)
        while carry:
            cur = res[k] + carry
            res[k] = cur % 10
            carry = cur // 10
            k += 1

    # Strip leading zeros (high-order end of the reversed list).
    while len(res) > 1 and res[-1] == 0:
        res.pop()

    digits = "".join(chr(d + 48) for d in reversed(res))
    return ("-" + digits) if neg else digits
