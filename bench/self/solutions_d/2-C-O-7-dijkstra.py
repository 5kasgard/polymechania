import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])
    heap = [(0, [src])]
    best = {src: 0}
    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node == dst:
            return (cost, path)
        if cost > best.get(node, float("inf")):
            continue
        for nxt, w in graph.get(node, []):
            ncost = cost + w
            if ncost < best.get(nxt, float("inf")) or (
                ncost == best.get(nxt, float("inf"))
            ):
                if ncost <= best.get(nxt, float("inf")):
                    best[nxt] = ncost
                    heapq.heappush(heap, (ncost, path + [nxt]))
    return None
