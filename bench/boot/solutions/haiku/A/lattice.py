# NOTE: none; O(k^2) over the blocked points after sorting, with factorial tables for binomials.
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

    n_max = h + w
    fact = [1] * (n_max + 1)
    for i in range(1, n_max + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (n_max + 1)
    inv_fact[n_max] = pow(fact[n_max], MOD - 2, MOD)
    for i in range(n_max, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def paths(dr: int, dc: int) -> int:
        if dr < 0 or dc < 0:
            return 0
        return fact[dr + dc] * inv_fact[dr] % MOD * inv_fact[dc] % MOD

    order = sorted(pts)
    dp = []
    for i, (r, c) in enumerate(order):
        v = paths(r, c)
        for j in range(i):
            rj, cj = order[j]
            if cj <= c:
                v -= dp[j] * paths(r - rj, c - cj)
        v %= MOD
        dp.append(v)

    ans = paths(h, w)
    for i, (r, c) in enumerate(order):
        ans -= dp[i] * paths(h - r, w - c)
    return ans % MOD
