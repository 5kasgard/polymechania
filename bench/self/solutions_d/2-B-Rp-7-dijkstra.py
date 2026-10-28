import heapq


def shortest_path(graph: dict[str, list[tuple[str, int]]], src: str, dst: str):
    if src == dst:
        return (0, [src])
    best = {}
    heap = [(0, [src])]
    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node in best:
            continue
        best[node] = (cost, path)
        if node == dst:
            return (cost, path)
        for nxt, w in graph.get(node, []):
            if nxt not in best:
                heapq.heappush(heap, (cost + w, path + [nxt]))
    return None
