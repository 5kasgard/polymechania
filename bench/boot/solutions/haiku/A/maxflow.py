from collections import deque


def max_flow(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    if s == t:
        raise ValueError("source and sink must be different")

    # Adjacency-list residual graph: edge 2k is forward, 2k+1 is its reverse.
    to = []
    cap = []
    adj = [[] for _ in range(n)]
    for u, v, c in edges:
        adj[u].append(len(to))
        to.append(v)
        cap.append(c)
        adj[v].append(len(to))
        to.append(u)
        cap.append(0)

    total = 0
    while True:
        # BFS to build level graph.
        level = [-1] * n
        level[s] = 0
        queue = deque([s])
        while queue:
            v = queue.popleft()
            for e in adj[v]:
                w = to[e]
                if cap[e] > 0 and level[w] < 0:
                    level[w] = level[v] + 1
                    queue.append(w)
        if level[t] < 0:
            break

        # Blocking flow with an iterative DFS (no recursion).
        it = [0] * n
        while True:
            path = []
            v = s
            while v != t:
                advanced = False
                while it[v] < len(adj[v]):
                    e = adj[v][it[v]]
                    w = to[e]
                    if cap[e] > 0 and level[w] == level[v] + 1:
                        path.append(e)
                        v = w
                        advanced = True
                        break
                    it[v] += 1
                if not advanced:
                    if v == s:
                        break
                    # Dead end: retreat and skip the edge that led here.
                    level[v] = -1
                    e = path.pop()
                    v = to[e ^ 1]
                    it[v] += 1
            if v != t:
                break
            f = min(cap[e] for e in path)
            for e in path:
                cap[e] -= f
                cap[e ^ 1] += f
            total += f

    return total
