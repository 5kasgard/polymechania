def multiply(a: str, b: str) -> str:
    # Sign: negative iff exactly one operand is negative.
    neg_a = a.startswith("-")
    neg_b = b.startswith("-")
    da = a[1:] if neg_a else a
    db = b[1:] if neg_b else b

    # Digit values, most significant first.
    xs = [ord(c) - 48 for c in da]
    ys = [ord(c) - 48 for c in db]
    n, m = len(xs), len(ys)

    # Accumulate partial products by position; carry once at the end.
    acc = [0] * (n + m)
    for i in range(n - 1, -1, -1):
        xi = xs[i]
        if xi == 0:
            continue
        for j in range(m - 1, -1, -1):
            acc[i + j + 1] += xi * ys[j]

    # Propagate carries from least significant position upward.
    carry = 0
    for k in range(n + m - 1, -1, -1):
        total = acc[k] + carry
        acc[k] = total % 10
        carry = total // 10
    # carry is always 0 here because n + m digits suffice.

    # Strip leading zeros, keeping a single "0" if everything is zero.
    start = 0
    while start < len(acc) - 1 and acc[start] == 0:
        start += 1
    digits = "".join(chr(d + 48) for d in acc[start:])

    if digits == "0":
        return "0"
    if neg_a != neg_b:
        return "-" + digits
    return digits
