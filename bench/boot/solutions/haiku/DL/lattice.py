from bisect import bisect_left

MOD = 1_000_000_007


def lattice_paths(h: int, w: int, blocked: list[tuple[int, int]]) -> int:
    # Count monotone lattice paths avoiding blocked points.
    # Total paths between two points: C(dr + dc, dr).
    # Blocked points are sorted in (row, col) order; dp over blocked points
    # counts paths from (0,0) to each blocked point that avoid earlier blocked points.
    # Only points inside the rectangle matter.
    if h < 0 or w < 0:
        return 0

    pts = sorted(set(
        (r, c) for (r, c) in blocked
        if 0 <= r <= h and 0 <= c <= w
    ))

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
        if dr < 0 or dc < 0:
            return 0
        return fact[dr + dc] * inv_fact[dr] % MOD * inv_fact[dc] % MOD

    # Add target as final point.
    targets = pts + [(h, w)]
    m = len(targets)
    dp = [0] * m
    for i, (r, c) in enumerate(targets):
        total = ways(r, c)
        for j in range(i):
            pr, pc = targets[j]
            if pr <= r and pc <= c and dp[j]:
                total -= dp[j] * ways(r - pr, c - pc)
        dp[i] = total % MOD

    # Blocked points get dp values that are paths reaching them; subtract them.
    # The answer is dp for (h, w).
    return dp[-1] % MOD
