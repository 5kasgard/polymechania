import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps)
    for n, ds in deps.items():
        nodes.update(ds)

    # Unique prerequisites per node, and reverse edges (prereq -> dependents).
    prereqs = {n: set() for n in nodes}
    dependents = {n: [] for n in nodes}
    for n, ds in deps.items():
        for d in set(ds):
            prereqs[n].add(d)
            dependents[d].append(n)

    remaining = {n: len(prereqs[n]) for n in nodes}
    heap = [n for n in nodes if remaining[n] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        n = heapq.heappop(heap)
        order.append(n)
        for m in dependents[n]:
            remaining[m] -= 1
            if remaining[m] == 0:
                heapq.heappush(heap, m)

    if len(order) != len(nodes):
        raise ValueError("cycle detected")
    return order
