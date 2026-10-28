import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])
    rev = {}
    zero = False
    for u, edges in graph.items():
        for v, w in edges:
            rev.setdefault(v, []).append((u, w))
            if w == 0:
                zero = True
    dist = {dst: 0}
    heap = [(0, dst)]
    while heap:
        d, v = heapq.heappop(heap)
        if d > dist.get(v, float("inf")):
            continue
        for u, w in rev.get(v, ()):
            nd = d + w
            if nd < dist.get(u, float("inf")):
                dist[u] = nd
                heapq.heappush(heap, (nd, u))
    if src not in dist:
        return None

    def tight(u):
        du = dist[u]
        res = set()
        for v, w in graph.get(u, ()):
            if v in dist and w + dist[v] == du:
                res.add(v)
        return sorted(res)

    def reaches(start, blocked):
        if start == dst:
            return True
        seen = {start}
        stack = [start]
        while stack:
            x = stack.pop()
            for y in tight(x):
                if y == dst:
                    return True
                if y in blocked or y in seen:
                    continue
                seen.add(y)
                stack.append(y)
        return False

    path = [src]
    on_path = {src}
    u = src
    while u != dst:
        nxt = None
        for v in tight(u):
            if v in on_path:
                continue
            if not zero or reaches(v, on_path):
                nxt = v
                break
        if nxt is None:
            return None
        path.append(nxt)
        on_path.add(nxt)
        u = nxt
    return (dist[src], path)
