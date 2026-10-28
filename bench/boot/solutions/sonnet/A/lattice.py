MOD = 1_000_000_007


def lattice_paths(h: int, w: int, blocked: list[tuple[int, int]]) -> int:
    if h < 0 or w < 0:
        return 0
    pts = set()
    for p in blocked:
        r, c = p[0], p[1]
        if 0 <= r <= h and 0 <= c <= w:
            pts.add((r, c))
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

    def comb(a, b):
        return fact[a] * inv[b] % MOD * inv[a - b] % MOD

    order = sorted(pts)
    order.append((h, w))
    m = len(order)
    dp = [0] * m
    for i in range(m):
        ri, ci = order[i]
        total = comb(ri + ci, ri)
        sub = 0
        for j in range(i):
            rj, cj = order[j]
            if cj <= ci:
                dr = ri - rj
                dc = ci - cj
                sub += dp[j] * (fact[dr + dc] * inv[dr] % MOD * inv[dc] % MOD)
        dp[i] = (total - sub) % MOD
    return dp[m - 1] % MOD
