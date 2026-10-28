def multiply(a: str, b: str) -> str:
    neg_a = a.startswith("-")
    neg_b = b.startswith("-")
    da = a[1:] if neg_a else a
    db = b[1:] if neg_b else b
    if da == "0" or db == "0" or not da or not db:
        return "0"

    K = 9
    BASE = 10 ** K

    def chunks(s):
        out = []
        i = len(s)
        while i > 0:
            j = max(0, i - K)
            out.append(int(s[j:i]))
            i = j
        return out

    A = chunks(da)
    B = chunks(db)
    if len(A) < len(B):
        A, B = B, A

    res = [0] * (len(A) + len(B) + 1)
    for j, y in enumerate(B):
        if y == 0:
            continue
        for i, x in enumerate(A):
            res[i + j] += x * y

    carry = 0
    for k in range(len(res)):
        v = res[k] + carry
        carry, res[k] = divmod(v, BASE)
    while carry:
        carry, r = divmod(carry, BASE)
        res.append(r)

    while len(res) > 1 and res[-1] == 0:
        res.pop()

    parts = [str(res[-1])]
    for k in range(len(res) - 2, -1, -1):
        parts.append(str(res[k]).zfill(K))
    s = "".join(parts)
    if neg_a != neg_b:
        s = "-" + s
    return s
