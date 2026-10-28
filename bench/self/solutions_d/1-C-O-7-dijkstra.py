import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    # Heap entries are (cost, path); tuple ordering breaks cost ties by the
    # lexicographically smallest path, as required.
    heap = [(0, [src])]
    settled = {}  # node -> (cost, path) once finalised

    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node in settled:
            continue
        settled[node] = (cost, path)
        if node == dst:
            return (cost, path)
        for nxt, w in graph.get(node, []):
            if nxt not in settled:
                heapq.heappush(heap, (cost + w, path + [nxt]))

    return None


if __name__ == '__main__':
    g = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
    }
    print(shortest_path(g, 'A', 'D'))  # (4, ['A', 'B', 'C', 'D'])
    print(shortest_path(g, 'A', 'A'))  # (0, ['A'])
    print(shortest_path(g, 'D', 'A'))  # None
