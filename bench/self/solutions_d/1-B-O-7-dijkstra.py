import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])
    best = {src: 0}
    heap = [(0, [src])]
    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node == dst:
            return (cost, path)
        if cost > best.get(node, float('inf')):
            continue
        for nxt, w in graph.get(node, []):
            ncost = cost + w
            if ncost < best.get(nxt, float('inf')) or (
                ncost == best.get(nxt, float('inf'))
            ):
                best[nxt] = min(ncost, best.get(nxt, float('inf')))
                heapq.heappush(heap, (ncost, path + [nxt]))
    return None


if __name__ == '__main__':
    g = {
        'a': [('b', 1), ('c', 4)],
        'b': [('c', 2), ('d', 5)],
        'c': [('d', 1)],
    }
    print(shortest_path(g, 'a', 'd'))
    print(shortest_path(g, 'a', 'a'))
    print(shortest_path(g, 'd', 'a'))
