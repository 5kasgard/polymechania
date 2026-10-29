def multiply(a: str, b: str) -> str:
    neg = (a[0] == '-') != (b[0] == '-')
    da = a.lstrip('-')
    db = b.lstrip('-')
    n, m = len(da), len(db)
    res = [0] * (n + m)
    for i in range(n - 1, -1, -1):
        x = ord(da[i]) - 48
        if x == 0:
            continue
        carry = 0
        for j in range(m - 1, -1, -1):
            cur = res[i + j + 1] + x * (ord(db[j]) - 48) + carry
            res[i + j + 1] = cur % 10
            carry = cur // 10
        res[i] += carry
    start = 0
    while start < len(res) - 1 and res[start] == 0:
        start += 1
    digits = ''.join(chr(48 + d) for d in res[start:])
    if digits == '0':
        return '0'
    return '-' + digits if neg else digits
