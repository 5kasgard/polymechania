import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    # Dijkstra over (cost, path) so that ties are broken by the
    # lexicographically smallest node list, as the spec requires.
    # Heap entries carry the full path; since paths are compared as lists
    # of strings, the heap naturally yields the smallest (cost, path) first.
    best = {}
    heap = [(0, [src])]
    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node in best:
            continue
        best[node] = (cost, path)
        if node == dst:
            return (cost, path)
        for nxt, w in graph.get(node, []):
            if nxt not in best:
                heapq.heappush(heap, (cost + w, path + [nxt]))
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
