import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    # Heap entries are (cost, path); comparing paths lexicographically
    # makes equal-cost ties resolve to the smallest node list first.
    heap = [(0, [src])]
    best = {src: 0}
    done = set()

    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node in done:
            continue
        done.add(node)
        if node == dst:
            return (cost, path)
        for nxt, w in graph.get(node, []):
            if nxt in done:
                continue
            ncost = cost + w
            known = best.get(nxt)
            if known is None or ncost <= known:
                best[nxt] = ncost
                heapq.heappush(heap, (ncost, path + [nxt]))

    return None
