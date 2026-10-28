import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    best = {src: 0}
    heap = [(0, [src])]
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
            if nxt not in best or ncost < best[nxt]:
                best[nxt] = ncost
                heapq.heappush(heap, (ncost, path + [nxt]))
            elif ncost == best[nxt]:
                heapq.heappush(heap, (ncost, path + [nxt]))

    return None
