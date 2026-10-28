import heapq
from collections import deque


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    rev = {}
    has_zero = False
    for u, edges in graph.items():
        for v, w in edges:
            rev.setdefault(v, []).append((u, w))
            if w == 0:
                has_zero = True

    # distances to dst, via reverse Dijkstra
    dtd = {dst: 0}
    heap = [(0, dst)]
    done = set()
    while heap:
        d, x = heapq.heappop(heap)
        if x in done:
            continue
        done.add(x)
        for u, w in rev.get(x, ()):
            nd = d + w
            if u not in dtd or nd < dtd[u]:
                dtd[u] = nd
                heapq.heappush(heap, (nd, u))

    if src not in dtd:
        return None

    total = dtd[src]
    path = [src]
    u = src

    if not has_zero:
        while u != dst:
            best = None
            du = dtd[u]
            for v, w in graph.get(u, ()):
                if v in dtd and w + dtd[v] == du:
                    if best is None or v < best:
                        best = v
            path.append(best)
            u = best
        return (total, path)

    visited = {src}
    while u != dst:
        # nodes that can reach dst via tight edges avoiding visited nodes
        can = {dst}
        dq = deque([dst])
        while dq:
            x = dq.popleft()
            dx = dtd[x]
            for p, w in rev.get(x, ()):
                if p in can or p in visited:
                    continue
                if p in dtd and dtd[p] == w + dx:
                    can.add(p)
                    dq.append(p)
        best = None
        du = dtd[u]
        for v, w in graph.get(u, ()):
            if v in can and v not in visited and w + dtd[v] == du:
                if best is None or v < best:
                    best = v
        path.append(best)
        visited.add(best)
        u = best
    return (total, path)
