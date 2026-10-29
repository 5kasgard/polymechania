import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # Collect every node, including those mentioned only as dependencies.
    nodes = set(deps.keys())
    for n, ds in deps.items():
        nodes.update(ds)

    # Build the graph: an edge d -> n for each dependency d of n.
    dependents = {v: [] for v in nodes}
    indegree = {v: 0 for v in nodes}
    for n, ds in deps.items():
        # Count each distinct dependency once, so duplicates don't skew indegree.
        for d in set(ds):
            dependents[d].append(n)
            indegree[n] += 1

    # Min-heap of ready nodes gives the alphabetically smallest ready node first.
    ready = [v for v in nodes if indegree[v] == 0]
    heapq.heapify(ready)

    order = []
    while ready:
        v = heapq.heappop(ready)
        order.append(v)
        for w in dependents[v]:
            indegree[w] -= 1
            if indegree[w] == 0:
                heapq.heappush(ready, w)

    if len(order) != len(nodes):
        raise ValueError("cycle detected")
    return order
