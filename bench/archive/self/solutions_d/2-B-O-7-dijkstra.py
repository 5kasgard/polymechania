import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])
    heap = [(0, [src])]
    best = {src: (0, [src])}
    settled = set()
    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node in settled:
            continue
        settled.add(node)
        if node == dst:
            return (cost, path)
        for nxt, w in graph.get(node, []):
            if nxt in settled:
                continue
            cand = (cost + w, path + [nxt])
            if nxt not in best or cand < best[nxt]:
                best[nxt] = cand
                heapq.heappush(heap, cand)
    return None
