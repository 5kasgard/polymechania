import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps.keys())
    for dlist in deps.values():
        nodes.update(dlist)

    # Edges: dependency -> dependent
    dependents: dict[str, list[str]] = {n: [] for n in nodes}
    indegree: dict[str, int] = {n: 0 for n in nodes}
    for n, dlist in deps.items():
        for d in set(dlist):
            dependents[d].append(n)
            indegree[n] += 1

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
        'app': ['lib', 'utils'],
        'lib': ['core'],
        'utils': ['core', 'base'],
    }
    print(topo_sort(demo))
    print(topo_sort({'b': ['a'], 'c': [], 'a': []}))
    try:
        topo_sort({'x': ['y'], 'y': ['x']})
    except ValueError as e:
        print('error:', e)
