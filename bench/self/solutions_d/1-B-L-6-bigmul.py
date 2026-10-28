def multiply(a: str, b: str) -> str:
    # Sign handling
    neg = (a[0] == '-') != (b[0] == '-')
    da = a.lstrip('-')
    db = b.lstrip('-')

    # Zero short-circuit so the result is "0", never "-0"
    if da == '0' or db == '0':
        return '0'

    la, lb = len(da), len(db)
    # Digits stored least-significant first
    ra = [ord(c) - 48 for c in reversed(da)]
    rb = [ord(c) - 48 for c in reversed(db)]
    res = [0] * (la + lb)

    # Schoolbook multiplication, carrying as we go
    for i in range(la):
        carry = 0
        ai = ra[i]
        for j in range(lb):
            cur = res[i + j] + ai * rb[j] + carry
            res[i + j] = cur % 10
            carry = cur // 10
        k = i + lb
        while carry:
            cur = res[k] + carry
            res[k] = cur % 10
            carry = cur // 10
            k += 1

    # Strip leading zeros (most significant end)
    while len(res) > 1 and res[-1] == 0:
        res.pop()

    digits = ''.join(chr(d + 48) for d in reversed(res))
    return ('-' + digits) if neg else digits
