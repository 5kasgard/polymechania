import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    # heap entries: (cost, path_list, node); path list gives the
    # lexicographic tie-break directly
    heap = [(0, [src], src)]
    settled = set()

    while heap:
        cost, path, node = heapq.heappop(heap)
        if node in settled:
            continue
        settled.add(node)
        if node == dst:
            return (cost, path)
        for nxt, w in graph.get(node, []):
            if nxt not in settled:
                heapq.heappush(heap, (cost + w, path + [nxt], nxt))

    return None
