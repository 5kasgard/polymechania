import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    # Dijkstra over (cost, path) so that ties are broken by the
    # lexicographically smallest node list, as the specification requires.
    # Keying the heap on (cost, path) makes the first time dst is popped the
    # cheapest and lexicographically smallest among those of minimal cost.
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
            if nxt not in best or ncost <= best[nxt]:
                best[nxt] = ncost
                heapq.heappush(heap, (ncost, path + [nxt]))

    return None


if __name__ == '__main__':
    g = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
        'D': [],
    }
    print(shortest_path(g, 'A', 'D'))   # (4, ['A', 'B', 'C', 'D'])
    print(shortest_path(g, 'A', 'A'))   # (0, ['A'])
    print(shortest_path(g, 'D', 'A'))   # None
    tie = {'S': [('X', 1), ('Y', 1)], 'X': [('T', 1)], 'Y': [('T', 1)], 'T': []}
    print(shortest_path(tie, 'S', 'T'))  # (2, ['S', 'X', 'T'])
