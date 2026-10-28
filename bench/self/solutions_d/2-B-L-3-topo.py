import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps.keys())
    for children in deps.values():
        nodes.update(children)

    # indegree[n] = number of distinct dependencies n is waiting on
    indegree = {n: 0 for n in nodes}
    # dependents[d] = nodes that depend on d
    dependents = {n: [] for n in nodes}
    for n, required in deps.items():
        for d in set(required):
            indegree[n] += 1
            dependents[d].append(n)

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
        raise ValueError("cycle detected")
    return order
