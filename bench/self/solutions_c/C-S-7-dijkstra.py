import heapq


def shortest_path(graph, src, dst):
    if src == dst:
        return (0, [src])

    heap = [(0, [src])]
    best = {src: 0}
    while heap:
        cost, path = heapq.heappop(heap)
        node = path[-1]
        if node == dst:
            return (cost, path)
        if cost > best.get(node, cost):
            continue
        for nxt, w in graph.get(node, []):
            ncost = cost + w
            if nxt not in best or ncost <= best[nxt]:
                best[nxt] = ncost
                heapq.heappush(heap, (ncost, path + [nxt]))
    return None


if __name__ == "__main__":
    g = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 2), ("D", 5)],
        "C": [("D", 1)],
        "D": [],
    }
    print(shortest_path(g, "A", "D"))
    print(shortest_path(g, "A", "A"))
    print(shortest_path(g, "D", "A"))
    print(shortest_path({"X": [("Y", 2)], "Y": [("X", 2)], "Z": []}, "X", "Z"))
