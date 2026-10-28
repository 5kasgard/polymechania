import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps)
    for ds in deps.values():
        nodes.update(ds)

    children: dict[str, list[str]] = {n: [] for n in nodes}
    indeg: dict[str, int] = {n: 0 for n in nodes}
    for n, ds in deps.items():
        for d in set(ds):
            children[d].append(n)
            indeg[n] += 1

    heap = [n for n in nodes if indeg[n] == 0]
    heapq.heapify(heap)

    order: list[str] = []
    while heap:
        m = heapq.heappop(heap)
        order.append(m)
        for c in children[m]:
            indeg[c] -= 1
            if indeg[c] == 0:
                heapq.heappush(heap, c)

    if len(order) != len(nodes):
        raise ValueError("cycle detected")
    return order
