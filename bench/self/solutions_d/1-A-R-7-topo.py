import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps.keys())
    for targets in deps.values():
        nodes.update(targets)

    # dependents[d] lists the nodes that depend on d
    dependents: dict[str, list[str]] = {n: [] for n in nodes}
    indegree: dict[str, int] = {n: 0 for n in nodes}
    for node, prereqs in deps.items():
        for p in set(prereqs):
            dependents[p].append(node)
            indegree[node] += 1

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


if __name__ == '__main__':
    demo = {
        "app": ["lib", "utils"],
        "lib": ["core"],
        "utils": ["core"],
        "tests": ["app"],
    }
    print("order:", topo_sort(demo))
    try:
        topo_sort({"a": ["b"], "b": ["a"]})
    except ValueError as e:
        print("cycle error:", e)
