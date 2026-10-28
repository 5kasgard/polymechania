def edit_script(a: str, b: str) -> list[tuple]:
    n, m = len(a), len(b)
    # dp[i][j] = Levenshtein distance between a[i:] and b[j:]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n and j == m:
                dp[i][j] = 0
            elif i == n:
                dp[i][j] = m - j
            elif j == m:
                dp[i][j] = n - i
            else:
                best = dp[i + 1][j] + 1
                best = min(best, dp[i][j + 1] + 1)
                cost = 0 if a[i] == b[j] else 1
                best = min(best, dp[i + 1][j + 1] + cost)
                dp[i][j] = best

    ops = []
    i = j = 0
    while i < n or j < m:
        if i < n and j < m:
            if a[i] == b[j] and dp[i][j] == dp[i + 1][j + 1]:
                ops.append(("keep", a[i]))
                i += 1
                j += 1
                continue
            if a[i] != b[j] and dp[i][j] == dp[i + 1][j + 1] + 1:
                ops.append(("sub", a[i], b[j]))
                i += 1
                j += 1
                continue
        if i < n and dp[i][j] == dp[i + 1][j] + 1:
            ops.append(("del", a[i]))
            i += 1
            continue
        ops.append(("ins", b[j]))
        j += 1
    return ops
