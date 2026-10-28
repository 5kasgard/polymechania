import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # Collect every node, including those mentioned only as dependencies.
    nodes = set(deps.keys())
    for targets in deps.values():
        nodes.update(targets)

    # children[d] lists nodes that depend on d; indegree[n] counts n's dependencies.
    children: dict[str, list[str]] = {n: [] for n in nodes}
    indegree: dict[str, int] = {n: 0 for n in nodes}
    for node, prereqs in deps.items():
        # Count each distinct prerequisite once, even if listed repeatedly.
        for p in set(prereqs):
            children[p].append(node)
            indegree[node] += 1

    # Min-heap of ready nodes yields the alphabetically smallest ready node first.
    ready = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(ready)

    order: list[str] = []
    while ready:
        n = heapq.heappop(ready)
        order.append(n)
        for c in children[n]:
            indegree[c] -= 1
            if indegree[c] == 0:
                heapq.heappush(ready, c)

    if len(order) != len(nodes):
        raise ValueError("dependency cycle detected")
    return order
