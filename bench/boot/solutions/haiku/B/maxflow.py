from collections import deque


def max_flow(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    if s == t:
        raise ValueError("source and sink must be different")

    graph = [[] for _ in range(n)]
    to: list[int] = []
    cap: list[int] = []

    def add_edge(u: int, v: int, c: int) -> None:
        graph[u].append(len(to))
        to.append(v)
        cap.append(c)
        graph[v].append(len(to))
        to.append(u)
        cap.append(0)

    total_cap = 0
    for u, v, c in edges:
        if u == v:
            continue  # self-loops never carry useful flow
        add_edge(u, v, c)
        total_cap += c

    inf = total_cap + 1

    def dfs(u: int, f: int, level: list[int], it: list[int]) -> int:
        if u == t:
            return f
        while it[u] < len(graph[u]):
            e = graph[u][it[u]]
            v = to[e]
            if cap[e] > 0 and level[v] == level[u] + 1:
                d = dfs(v, min(f, cap[e]), level, it)
                if d > 0:
                    cap[e] -= d
                    cap[e ^ 1] += d
                    return d
            it[u] += 1
        return 0

    flow = 0
    while True:
        level = [-1] * n
        level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for e in graph[u]:
                v = to[e]
                if cap[e] > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    q.append(v)
        if level[t] < 0:
            return flow

        it = [0] * n
        while True:
            f = dfs(s, inf, level, it)
            if f == 0:
                break
            flow += f
