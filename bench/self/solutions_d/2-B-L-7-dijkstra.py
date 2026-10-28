import heapq


def shortest_path(graph: dict[str, list[tuple[str, int]]], src: str, dst: str):
    if src == dst:
        return (0, [src])

    # Nodes appearing only as edge targets have no outgoing edges.
    def neighbours(node):
        return graph.get(node, [])

    # Heap entries are (cost, path); path is a list, so ties in cost are
    # broken by lexicographically smallest path, as required.
    heap = [(0, [src])]
    best = {src: (0, [src])}  # node -> (cost, path) of best settled label
    settled = set()

    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node in settled:
            continue
        settled.add(node)
        if node == dst:
            return (cost, path)
        for nxt, w in neighbours(node):
            if nxt in settled:
                continue
            new_cost = cost + w
            new_path = path + [nxt]
            old = best.get(nxt)
            if old is None or (new_cost, new_path) < old:
                best[nxt] = (new_cost, new_path)
                heapq.heappush(heap, (new_cost, new_path))

    return None
