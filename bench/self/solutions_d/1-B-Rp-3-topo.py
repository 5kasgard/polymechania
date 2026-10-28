import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps.keys())
    for targets in deps.values():
        nodes.update(targets)

    indegree = {n: 0 for n in nodes}
    dependents = {n: [] for n in nodes}
    for node, prereqs in deps.items():
        for p in set(prereqs):
            indegree[node] += 1
            dependents[p].append(node)

    heap = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        n = heapq.heappop(heap)
        order.append(n)
        for d in dependents[n]:
            indegree[d] -= 1
            if indegree[d] == 0:
                heapq.heappush(heap, d)

    if len(order) != len(nodes):
        raise ValueError("cycle detected")
    return order
