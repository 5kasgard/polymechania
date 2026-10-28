import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    # Dijkstra with lexicographic tie-breaking on the full path.
    # Heap entries: (cost, path_list). Comparing (cost, path) orders by
    # cheapest cost first, then lexicographically smallest path, so the
    # first time dst is popped it carries the required answer.
    # Each node is finalised once; we store the best (cost, path) seen.
    best = {src: (0, [src])}
    heap = [(0, [src])]
    done = set()

    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node in done:
            continue
        if best.get(node) != (cost, path):
            continue
        done.add(node)
        if node == dst:
            return (cost, path)
        for nbr, w in graph.get(node, []):
            if nbr in done:
                continue
            ncost = cost + w
            npath = path + [nbr]
            cur = best.get(nbr)
            if cur is None or (ncost, npath) < cur:
                best[nbr] = (ncost, npath)
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
    tie = {'S': [('X', 1), ('Y', 1)], 'X': [('T', 1)], 'Y': [('T', 1)], 'T': []}
    print(shortest_path(tie, 'S', 'T')) # (2, ['S', 'X', 'T'])
