import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps.keys())
    for targets in deps.values():
        nodes.update(targets)

    # children[d] = nodes that depend on d; indegree[n] = number of unmet dependencies of n
    children: dict[str, list[str]] = {n: [] for n in nodes}
    indegree: dict[str, int] = {n: 0 for n in nodes}
    for node, reqs in deps.items():
        # Treat repeated dependency entries as one edge so counts stay consistent.
        for req in set(reqs):
            children[req].append(node)
            indegree[node] += 1

    heap = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(heap)

    order: list[str] = []
    while heap:
        n = heapq.heappop(heap)
        order.append(n)
        for child in children[n]:
            indegree[child] -= 1
            if indegree[child] == 0:
                heapq.heappush(heap, child)

    if len(order) != len(nodes):
        raise ValueError("cycle detected")
    return order
