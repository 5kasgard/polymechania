from collections import deque


def max_flow(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    if s == t:
        raise ValueError("source and sink must differ")

    # Adjacency with paired residual edges: edge i and i^1 are reverses.
    to = []
    cap = []
    adj = [[] for _ in range(n)]

    def add(u: int, v: int, c: int) -> None:
        adj[u].append(len(to))
        to.append(v)
        cap.append(c)
        adj[v].append(len(to))
        to.append(u)
        cap.append(0)

    for u, v, c in edges:
        if u == v:
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
            for e in adj[x]:
                if cap[e] > 0 and level[to[e]] < 0:
                    level[to[e]] = level[x] + 1
                    q.append(to[e])
        if level[t] < 0:
            break

        it = [0] * n

        # Iterative DFS for blocking flow.
        def dfs_push() -> int:
            total = 0
            while True:
                # Find an augmenting path with an explicit stack.
                stack_nodes = [s]
                stack_edges = []
                found = False
                while stack_nodes:
                    x = stack_nodes[-1]
                    if x == t:
                        found = True
                        break
                    advanced = False
                    while it[x] < len(adj[x]):
                        e = adj[x][it[x]]
                        y = to[e]
                        if cap[e] > 0 and level[y] == level[x] + 1:
                            stack_nodes.append(y)
                            stack_edges.append(e)
                            advanced = True
                            break
                        it[x] += 1
                    if not advanced:
                        stack_nodes.pop()
                        if stack_edges:
                            stack_edges.pop()
                            # Dead end: advance the parent's pointer.
                            px = stack_nodes[-1]
                            it[px] += 1
                if not found:
                    return total
                push = min(cap[e] for e in stack_edges)
                for e in stack_edges:
                    cap[e] -= push
                    cap[e ^ 1] += push
                total += push
                # Restart from source; saturated edges will be skipped
                # because their residual capacity is now zero.

        flow += dfs_push()

    return flow
