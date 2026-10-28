def multiply(a: str, b: str) -> str:
    neg = (a[0] == "-") != (b[0] == "-")
    da = a[1:] if a[0] == "-" else a
    db = b[1:] if b[0] == "-" else b

    if da == "0" or db == "0":
        return "0"

    na, nb = len(da), len(db)
    acc = [0] * (na + nb)

    # Digits in reverse order so index i corresponds to 10**i.
    ra = [ord(c) - 48 for c in reversed(da)]
    rb = [ord(c) - 48 for c in reversed(db)]

    for i, x in enumerate(ra):
        if x == 0:
            continue
        for j, y in enumerate(rb):
            acc[i + j] += x * y

    # Single carry-propagation pass.
    carry = 0
    for k in range(na + nb):
        total = acc[k] + carry
        acc[k] = total % 10
        carry = total // 10
    while carry:
        acc.append(carry % 10)
        carry //= 10

    # Strip leading zeros (from the high end) and build the string.
    while len(acc) > 1 and acc[-1] == 0:
        acc.pop()

    digits = "".join(chr(d + 48) for d in reversed(acc))
    return ("-" + digits) if neg else digits
