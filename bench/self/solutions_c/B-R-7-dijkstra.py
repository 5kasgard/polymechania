import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    # Dijkstra with lexicographic tie-breaking on the full path.
    # Heap entries: (cost, path_list). Popping the minimum (cost, path)
    # yields the cheapest path, and among equal costs the lexicographically
    # smallest node list, so the first time dst is popped is the answer.
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


if __name__ == '__main__':
    g = {
        'a': [('b', 1), ('c', 4)],
        'b': [('c', 2), ('d', 5)],
        'c': [('d', 1)],
        'd': [],
    }
    print(shortest_path(g, 'a', 'd'))   # (4, ['a', 'b', 'c', 'd'])
    print(shortest_path(g, 'a', 'a'))   # (0, ['a'])
    print(shortest_path(g, 'd', 'a'))   # None
    tie = {'s': [('x', 1), ('y', 1)], 'x': [('t', 1)], 'y': [('t', 1)], 't': []}
    print(shortest_path(tie, 's', 't'))  # (2, ['s', 'x', 't'])
