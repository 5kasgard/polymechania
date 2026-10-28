def multiply(a: str, b: str) -> str:
    # Sign handling: product is negative iff exactly one operand is negative.
    neg = (a[0] == "-") != (b[0] == "-")
    da = a.lstrip("-")
    db = b.lstrip("-")

    # Zero shortcut keeps the output as "0", never "-0".
    if da == "0" or db == "0":
        return "0"

    na, nb = len(da), len(db)
    # Accumulator for partial products, one slot per output digit position.
    acc = [0] * (na + nb)

    # Schoolbook multiplication working directly on digit characters.
    for i in range(na - 1, -1, -1):
        ai = ord(da[i]) - 48
        for j in range(nb - 1, -1, -1):
            bj = ord(db[j]) - 48
            acc[i + j + 1] += ai * bj

    # Single carry-propagation pass from the least significant position.
    carry = 0
    for k in range(na + nb - 1, -1, -1):
        total = acc[k] + carry
        acc[k] = total % 10
        carry = total // 10

    # Convert digits to characters, dropping leading zeros.
    digits = "".join(chr(d + 48) for d in acc).lstrip("0")
    if not digits:
        return "0"
    return "-" + digits if neg else digits
