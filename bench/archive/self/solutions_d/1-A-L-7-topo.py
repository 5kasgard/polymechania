import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # Collect every node, including those mentioned only as dependencies.
    nodes = set(deps)
    for n, ds in deps.items():
        nodes.update(ds)

    # dependents[d] lists nodes that depend on d; indegree[n] counts n's dependencies.
    dependents: dict[str, list[str]] = {n: [] for n in nodes}
    indegree: dict[str, int] = {n: 0 for n in nodes}
    for n, ds in deps.items():
        # Count each distinct dependency once, so duplicates don't skew the count.
        for d in set(ds):
            dependents[d].append(n)
            indegree[n] += 1

    heap = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(heap)

    order: list[str] = []
    while heap:
        n = heapq.heappop(heap)
        order.append(n)
        for m in dependents[n]:
            indegree[m] -= 1
            if indegree[m] == 0:
                heapq.heappush(heap, m)

    if len(order) != len(nodes):
        raise ValueError("cycle detected")
    return order
