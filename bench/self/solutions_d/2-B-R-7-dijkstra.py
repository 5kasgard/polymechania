import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    # Dijkstra with lexicographic tie-breaking on the full path.
    # Heap entries: (cost, path_list). Popping the smallest (cost, path)
    # yields, for each node, the cheapest path that is lexicographically
    # smallest among the cheapest, because path comparison is exactly the
    # tie rule the spec asks for, and prefixes are compared before extensions.
    best = {src: (0, [src])}
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
            npath = path + [nxt]
            cur = best.get(nxt)
            if cur is None or (ncost, npath) < cur:
                best[nxt] = (ncost, npath)
                heapq.heappush(heap, (ncost, npath))

    return None


if __name__ == '__main__':
    g = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
        'D': [],
    }
    print(shortest_path(g, 'A', 'D'))   # (4, ['A', 'B', 'C', 'D'])
    print(shortest_path(g, 'D', 'A'))   # None
    print(shortest_path(g, 'A', 'A'))   # (0, ['A'])

    tie = {
        'S': [('X', 1), ('Y', 1)],
        'X': [('T', 1)],
        'Y': [('T', 1)],
    }
    print(shortest_path(tie, 'S', 'T'))  # (2, ['S', 'X', 'T'])
