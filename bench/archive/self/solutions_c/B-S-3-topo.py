import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # Collect every node, including those mentioned only as dependencies.
    nodes = set(deps.keys())
    for targets in deps.values():
        nodes.update(targets)

    # dependents[d] = nodes that depend on d; indegree[n] = number of
    # distinct dependencies of n still unprocessed.
    dependents = {n: [] for n in nodes}
    indegree = {n: 0 for n in nodes}
    for node, targets in deps.items():
        for d in set(targets):  # ignore duplicate listings
            dependents[d].append(node)
            indegree[node] += 1

    heap = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        n = heapq.heappop(heap)
        order.append(n)
        for m in dependents[n]:
            indegree[m] -= 1
            if indegree[m] == 0:
                heapq.heappush(heap, m)

    if len(order) != len(nodes):
        raise ValueError("dependency cycle detected")
    return order
