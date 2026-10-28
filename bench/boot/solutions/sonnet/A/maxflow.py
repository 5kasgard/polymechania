from collections import deque


def max_flow(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    if s == t:
        raise ValueError("source and sink must differ")
    to = []
    cap = []
    adj = [[] for _ in range(n)]
    for u, v, c in edges:
        if u == v or c <= 0:
            continue
        adj[u].append(len(to))
        to.append(v)
        cap.append(c)
        adj[v].append(len(to))
        to.append(u)
        cap.append(0)

    total = 0
    while True:
        level = [-1] * n
        level[s] = 0
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for e in adj[u]:
                v = to[e]
                if cap[e] > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    dq.append(v)
        if level[t] < 0:
            break
        it = [0] * n
        path = []
        u = s
        while True:
            if u == t:
                f = min(cap[e] for e in path)
                total += f
                first = -1
                for i, e in enumerate(path):
                    cap[e] -= f
                    cap[e ^ 1] += f
                    if first < 0 and cap[e] == 0:
                        first = i
                u = to[path[first] ^ 1]
                del path[first:]
                continue
            au = adj[u]
            i = it[u]
            lu = level[u] + 1
            found = -1
            while i < len(au):
                e = au[i]
                if cap[e] > 0 and level[to[e]] == lu:
                    found = e
                    break
                i += 1
            it[u] = i
            if found >= 0:
                path.append(found)
                u = to[found]
            else:
                if u == s:
                    break
                level[u] = -1
                e = path.pop()
                u = to[e ^ 1]
                it[u] += 1
    return total
