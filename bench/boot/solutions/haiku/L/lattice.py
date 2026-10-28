MOD = 1_000_000_007


def lattice_paths(h: int, w: int, blocked: list[tuple[int, int]]) -> int:
    pts = {(r, c) for (r, c) in blocked if 0 <= r <= h and 0 <= c <= w}
    if (0, 0) in pts or (h, w) in pts:
        return 0

    n = h + w
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv = [1] * (n + 1)
    inv[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % MOD

    def paths(dr: int, dc: int) -> int:
        if dr < 0 or dc < 0:
            return 0
        return fact[dr + dc] * inv[dr] % MOD * inv[dc] % MOD

    order = sorted(pts)
    k = len(order)
    f = [0] * k
    for i in range(k):
        ri, ci = order[i]
        val = paths(ri, ci)
        for j in range(i):
            rj, cj = order[j]
            if rj <= ri and cj <= ci and f[j]:
                val -= f[j] * paths(ri - rj, ci - cj)
        f[i] = val % MOD

    total = paths(h, w)
    for i in range(k):
        ri, ci = order[i]
        total -= f[i] * paths(h - ri, w - ci)
    return total % MOD
