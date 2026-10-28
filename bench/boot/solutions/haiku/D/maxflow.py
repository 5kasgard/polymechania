from collections import deque


def max_flow(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    if s == t:
        raise ValueError("source and sink must differ")

    # Adjacency via paired residual arcs: arc i and i^1 are reverses.
    head = [[] for _ in range(n)]
    to = []
    cap = []

    def add(u: int, v: int, c: int) -> None:
        head[u].append(len(to))
        to.append(v)
        cap.append(c)
        head[v].append(len(to))
        to.append(u)
        cap.append(0)

    for u, v, c in edges:
        if u == v or c == 0:
            continue
        add(u, v, c)

    flow = 0
    while True:
        # BFS to build level graph (Dinic).
        level = [-1] * n
        level[s] = 0
        q = deque([s])
        while q:
            x = q.popleft()
            for e in head[x]:
                if cap[e] > 0 and level[to[e]] < 0:
                    level[to[e]] = level[x] + 1
                    q.append(to[e])
        if level[t] < 0:
            break

        it = [0] * n

        def dfs(x: int, f: int) -> int:
            if x == t:
                return f
            while it[x] < len(head[x]):
                e = head[x][it[x]]
                y = to[e]
                if cap[e] > 0 and level[y] == level[x] + 1:
                    d = dfs(y, min(f, cap[e]))
                    if d > 0:
                        cap[e] -= d
                        cap[e ^ 1] += d
                        return d
                it[x] += 1
            return 0

        INF = float("inf")
        while True:
            f = dfs(s, 10**30)
            if f == 0:
                break
            flow += f

    return flow
