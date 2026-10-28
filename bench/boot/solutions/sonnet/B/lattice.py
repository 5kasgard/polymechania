def lattice_paths(h: int, w: int, blocked: list[tuple[int, int]]) -> int:
    MOD = 1_000_000_007
    if h < 0 or w < 0:
        return 0
    pts = set()
    for r, c in blocked:
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

    lst = sorted(pts)
    lst.append((h, w))
    k = len(lst)
    dp = [0] * k
    for i in range(k):
        ri, ci = lst[i]
        v = comb(ri + ci, ri)
        for j in range(i):
            rj, cj = lst[j]
            if cj <= ci and rj <= ri:
                dr = ri - rj
                dc = ci - cj
                v -= dp[j] * (fact[dr + dc] * inv[dr] % MOD * inv[dc] % MOD)
        dp[i] = v % MOD
    return dp[k - 1] % MOD
