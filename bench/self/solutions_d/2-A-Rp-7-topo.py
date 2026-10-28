import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps.keys())
    for targets in deps.values():
        nodes.update(targets)

    dependents: dict[str, set[str]] = {n: set() for n in nodes}
    indegree: dict[str, int] = {n: 0 for n in nodes}

    for node, prereqs in deps.items():
        for prereq in set(prereqs):
            dependents[prereq].add(node)
            indegree[node] += 1

    heap = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(heap)

    order: list[str] = []
    while heap:
        current = heapq.heappop(heap)
        order.append(current)
        for child in dependents[current]:
            indegree[child] -= 1
            if indegree[child] == 0:
                heapq.heappush(heap, child)

    if len(order) != len(nodes):
        raise ValueError("dependency graph contains a cycle")
    return order


if __name__ == '__main__':
    print("Demo 1:", topo_sort({"app": ["lib", "util"], "lib": ["util"], "util": []}))
    print("Demo 2:", topo_sort({"b": ["a"], "c": ["a"], "d": ["b", "c"]}))
    try:
        topo_sort({"x": ["y"], "y": ["x"]})
    except ValueError as exc:
        print("Demo 3 (cycle):", exc)
