import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    # Heap entries are (cost, path); path is a list of nodes from src.
    # Ordering by (cost, path) makes the lexicographically smallest
    # path win among equally cheap ones.
    heap = [(0, [src])]
    settled = set()

    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node in settled:
            continue
        settled.add(node)

        if node == dst:
            return (cost, path)

        for neighbour, weight in graph.get(node, []):
            if neighbour not in settled:
                heapq.heappush(heap, (cost + weight, path + [neighbour]))

    return None
