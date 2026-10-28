def multiply(a: str, b: str) -> str:
    neg = False
    if a.startswith('-'):
        neg = not neg
        a = a[1:]
    if b.startswith('-'):
        neg = not neg
        b = b[1:]

    # Digits least-significant first.
    ra = [ord(c) - 48 for c in reversed(a)]
    rb = [ord(c) - 48 for c in reversed(b)]
    n, m = len(ra), len(rb)

    # Schoolbook multiplication on digits. Column sums are kept unnormalised
    # and carries are propagated once at the end.
    acc = [0] * (n + m)
    for i, x in enumerate(ra):
        if x == 0:
            continue
        acc[i:i + m] = [p + x * q for p, q in zip(acc[i:i + m], rb)]

    digits = []
    carry = 0
    for col in acc:
        t = col + carry
        digits.append(t % 10)
        carry = t // 10
    while carry:
        digits.append(carry % 10)
        carry //= 10

    # Strip leading zeros (most significant digits are at the end).
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()

    s = ''.join(str(d) for d in reversed(digits))
    if s == '0':
        return '0'
    return '-' + s if neg else s
