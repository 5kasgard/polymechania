import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps)
    for targets in deps.values():
        nodes.update(targets)

    # Build reverse adjacency (dependency -> nodes that need it) and in-degrees.
    needed_by = {n: [] for n in nodes}
    indegree = {n: 0 for n in nodes}
    for node, reqs in deps.items():
        for r in set(reqs):
            needed_by[r].append(node)
            indegree[node] += 1

    heap = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        n = heapq.heappop(heap)
        order.append(n)
        for m in needed_by[n]:
            indegree[m] -= 1
            if indegree[m] == 0:
                heapq.heappush(heap, m)

    if len(order) != len(nodes):
        raise ValueError("cycle detected")
    return order


if __name__ == '__main__':
    deps = {
        'app': ['lib', 'utils'],
        'lib': ['core'],
        'utils': ['core'],
        'core': [],
    }
    print(topo_sort(deps))  # ['core', 'lib', 'utils', 'app']

    deps2 = {'b': ['a'], 'c': ['a'], 'a': []}
    print(topo_sort(deps2))  # ['a', 'b', 'c']

    try:
        topo_sort({'x': ['y'], 'y': ['x']})
    except ValueError as e:
        print('error:', e)  # error: cycle detected
