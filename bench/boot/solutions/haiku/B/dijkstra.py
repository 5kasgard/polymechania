import heapq


def shortest_path(graph: dict[str, list[tuple[str, int]]], src: str, dst: str):
    if src == dst:
        return (0, [src])

    # Heap entries are (cost, path); tuple ordering gives cheapest first,
    # then lexicographically smallest node sequence among equal costs.
    heap = [(0, (src,))]
    done = set()

    while heap:
        cost, path = heapq.heappop(heap)
        u = path[-1]
        if u in done:
            continue
        done.add(u)
        if u == dst:
            return (cost, list(path))
        onpath = set(path)
        for v, w in graph.get(u, ()):
            if v in done or v in onpath:
                continue
            heapq.heappush(heap, (cost + w, path + (v,)))

    return None
