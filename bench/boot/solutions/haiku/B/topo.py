import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps)
    for lst in deps.values():
        nodes.update(lst)

    dependents = {v: [] for v in nodes}
    indegree = {v: 0 for v in nodes}
    for n, lst in deps.items():
        for d in set(lst):
            dependents[d].append(n)
            indegree[n] += 1

    heap = [v for v in nodes if indegree[v] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        v = heapq.heappop(heap)
        order.append(v)
        for m in dependents[v]:
            indegree[m] -= 1
            if indegree[m] == 0:
                heapq.heappush(heap, m)

    if len(order) != len(nodes):
        raise ValueError("cycle detected")
    return order
