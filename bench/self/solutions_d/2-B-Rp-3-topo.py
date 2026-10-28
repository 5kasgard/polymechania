import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps)
    for targets in deps.values():
        nodes.update(targets)

    # Each node points to the nodes that depend on it.
    dependents: dict[str, set[str]] = {n: set() for n in nodes}
    indegree: dict[str, int] = {n: 0 for n in nodes}
    for node, prereqs in deps.items():
        for pre in set(prereqs):
            dependents[pre].add(node)
            indegree[node] += 1

    heap = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(heap)

    order: list[str] = []
    while heap:
        n = heapq.heappop(heap)
        order.append(n)
        for child in dependents[n]:
            indegree[child] -= 1
            if indegree[child] == 0:
                heapq.heappush(heap, child)

    if len(order) != len(nodes):
        raise ValueError("cycle detected")
    return order
