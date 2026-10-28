from collections import deque


def max_flow(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    if s == t:
        raise ValueError("source and sink must be different")

    # Adjacency via paired arc arrays: arc i and i^1 are reverse of each other.
    head = [[] for _ in range(n)]
    to = []
    cap = []
    for u, v, c in edges:
        head[u].append(len(to))
        to.append(v)
        cap.append(c)
        head[v].append(len(to))
        to.append(u)
        cap.append(0)

    total = 0
    INF = float("inf")

    while True:
        # BFS to build level graph.
        level = [-1] * n
        level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for e in head[u]:
                if cap[e] > 0 and level[to[e]] < 0:
                    level[to[e]] = level[u] + 1
                    q.append(to[e])
        if level[t] < 0:
            break

        it = [0] * n

        def dfs(u, f):
            # Depth bounded by number of levels, at most n (<= 500).
            if u == t:
                return f
            while it[u] < len(head[u]):
                e = head[u][it[u]]
                v = to[e]
                if cap[e] > 0 and level[v] == level[u] + 1:
                    d = dfs(v, min(f, cap[e]))
                    if d > 0:
                        cap[e] -= d
                        cap[e ^ 1] += d
                        return d
                it[u] += 1
            return 0

        while True:
            pushed = dfs(s, INF)
            if pushed <= 0:
                break
            total += int(pushed)

    return total
