MOD = 1_000_000_007


def lattice_paths(h: int, w: int, blocked: list[tuple[int, int]]) -> int:
    # Sort blocked points inside the rectangle; dp over them with
    # inclusion-exclusion: paths to each point avoiding earlier blocked points.
    if h < 0 or w < 0:
        return 0

    pts = set()
    for r, c in blocked:
        if 0 <= r <= h and 0 <= c <= w:
            pts.add((r, c))

    if (0, 0) in pts or (h, w) in pts:
        return 0

    # Factorials up to h + w
    n = h + w
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def ways(dr: int, dc: int) -> int:
        if dr < 0 or dc < 0:
            return 0
        return fact[dr + dc] * inv_fact[dr] % MOD * inv_fact[dc] % MOD

    # Order points so that every point comes after any point it can be reached from.
    order = sorted(pts)
    # Include the target as a final node.
    nodes = order + [(h, w)]
    m = len(nodes)
    dp = [0] * m
    for i, (r, c) in enumerate(nodes):
        total = ways(r, c)
        for j in range(i):
            rj, cj = nodes[j]
            if rj <= r and cj <= c and (rj, cj) != (r, c):
                total -= dp[j] * ways(r - rj, c - cj)
        dp[i] = total % MOD

    return dp[m - 1] % MOD
