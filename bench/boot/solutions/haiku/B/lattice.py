# NOTE: none; the work is O(k^2) over the k blocked points plus factorial tables up to h+w.
from math import comb


def lattice_paths(h: int, w: int, blocked: list[tuple[int, int]]) -> int:
    MOD = 1_000_000_007

    pts = {(r, c) for (r, c) in blocked if 0 <= r <= h and 0 <= c <= w}
    if (0, 0) in pts or (h, w) in pts:
        return 0

    n = h + w
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def ways(dr: int, dc: int) -> int:
        # number of monotone paths moving dr down and dc right
        if dr < 0 or dc < 0:
            return 0
        return fact[dr + dc] * inv_fact[dr] % MOD * inv_fact[dc] % MOD

    order = sorted(pts)
    order.append((h, w))

    # g[i]: paths from (0,0) to order[i] that touch no blocked point before it
    g = []
    for i, (r, c) in enumerate(order):
        val = ways(r, c)
        for j in range(i):
            qr, qc = order[j]
            if qr <= r and qc <= c:
                val -= g[j] * ways(r - qr, c - qc)
        g.append(val % MOD)

    return g[-1]
