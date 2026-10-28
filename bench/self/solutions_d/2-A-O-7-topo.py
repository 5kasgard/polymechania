import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps)
    for n, ds in deps.items():
        nodes.update(ds)

    # Unique dependencies per node, so duplicates do not skew in-degrees.
    preds: dict[str, set[str]] = {n: set() for n in nodes}
    dependents: dict[str, list[str]] = {n: [] for n in nodes}
    for n, ds in deps.items():
        for d in ds:
            if d not in preds[n]:
                preds[n].add(d)
                dependents[d].append(n)

    indeg = {n: len(preds[n]) for n in nodes}
    heap = [n for n in nodes if indeg[n] == 0]
    heapq.heapify(heap)

    order: list[str] = []
    while heap:
        n = heapq.heappop(heap)
        order.append(n)
        for m in dependents[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                heapq.heappush(heap, m)

    if len(order) != len(nodes):
        raise ValueError("dependency cycle detected")
    return order
