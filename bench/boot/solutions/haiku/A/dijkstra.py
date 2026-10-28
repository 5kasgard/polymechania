import heapq


def shortest_path(graph: dict[str, list[tuple[str, int]]], src: str, dst: str):
    # Heap entries are (cost, path, node). Popping in (cost, path) order means the
    # first time a node is popped it carries the cheapest, then lexicographically
    # smallest, simple path from src. Settled nodes are never expanded again.
    heap = [(0, [src], src)]
    settled = set()
    while heap:
        cost, path, node = heapq.heappop(heap)
        if node in settled:
            continue
        settled.add(node)
        if node == dst:
            return cost, path
        for nxt, w in graph.get(node, []):
            if nxt in settled or nxt in path:
                continue
            heapq.heappush(heap, (cost + w, path + [nxt], nxt))
    return None
