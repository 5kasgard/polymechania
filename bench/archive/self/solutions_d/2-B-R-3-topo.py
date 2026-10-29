import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps)
    for lst in deps.values():
        nodes.update(lst)

    indegree = {n: 0 for n in nodes}
    dependents = {n: [] for n in nodes}
    for node, lst in deps.items():
        for d in set(lst):
            indegree[node] += 1
            dependents[d].append(node)

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
