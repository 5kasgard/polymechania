def multiply(a: str, b: str) -> str:
    # Parse sign and digits.
    neg_a = a.startswith("-")
    neg_b = b.startswith("-")
    da = a[1:] if neg_a else a
    db = b[1:] if neg_b else b

    # Zero short-circuit (covers "0", "-0" inputs too).
    if da == "0" or db == "0":
        return "0"

    na, nb = len(da), len(db)
    # Digit values, most significant first.
    ra = [ord(c) - 48 for c in reversed(da)]  # least significant first
    rb = [ord(c) - 48 for c in reversed(db)]

    # Accumulate products into position buckets; carries are resolved after.
    acc = [0] * (na + nb)
    for i, x in enumerate(ra):
        if x == 0:
            continue
        for j, y in enumerate(rb):
            acc[i + j] += x * y

    # Propagate carries.
    carry = 0
    for k in range(na + nb):
        total = acc[k] + carry
        acc[k] = total % 10
        carry = total // 10
    # carry is always 0 here since the product fits in na+nb digits.

    # Strip leading zeros (most significant end).
    k = na + nb - 1
    while k > 0 and acc[k] == 0:
        k -= 1
    digits = "".join(chr(48 + acc[i]) for i in range(k, -1, -1))

    negative = neg_a != neg_b
    return "-" + digits if negative else digits
