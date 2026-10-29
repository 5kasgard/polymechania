import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    # Nodes that appear only as edge targets have no outgoing entry.
    # Build the set of all nodes so the search can still reach them.
    best = {src: (0, [src])}
    heap = [(0, [src], src)]
    # Each heap item is (cost, path, node). Ordering by (cost, path) makes
    # the first time dst is popped the cheapest path with the
    # lexicographically smallest node list among equal costs.
    settled = set()

    while heap:
        cost, path, node = heapq.heappop(heap)
        if node in settled:
            continue
        settled.add(node)
        if node == dst:
            return (cost, path)
        for nxt, w in graph.get(node, []):
            if nxt in settled:
                continue
            ncost = cost + w
            npath = path + [nxt]
            cur = best.get(nxt)
            if cur is None or (ncost, npath) < cur:
                best[nxt] = (ncost, npath)
                heapq.heappush(heap, (ncost, npath, nxt))

    return None
