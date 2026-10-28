import heapq


def shortest_path(graph: dict[str, list[tuple[str, int]]], src: str, dst: str):
    if src == dst:
        return (0, [src])

    # Heap entries are (cost, path_list). Ordering by (cost, path) means the
    # first time dst is popped, its path is cheapest and, among equally cheap
    # paths, lexicographically smallest.
    heap = [(0, [src])]
    # best[node] = the smallest (cost, path) already finalized for node.
    settled = {}

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
        'a': [('b', 1), ('c', 4)],
        'b': [('c', 2), ('d', 5)],
        'c': [('d', 1)],
        'd': [],
    }
    print(shortest_path(g, 'a', 'd'))   # (4, ['a', 'b', 'c', 'd'])
    print(shortest_path(g, 'a', 'a'))   # (0, ['a'])
    print(shortest_path(g, 'd', 'a'))   # None
