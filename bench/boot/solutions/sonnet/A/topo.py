import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set()
    for n, ds in deps.items():
        nodes.add(n)
        for d in ds:
            nodes.add(d)

    # Unique dependencies per node
    dep_sets = {n: set() for n in nodes}
    for n, ds in deps.items():
        dep_sets[n].update(ds)

    indegree = {n: len(dep_sets[n]) for n in nodes}
    dependents = {n: [] for n in nodes}
    for n, ds in dep_sets.items():
        for d in ds:
            dependents[d].append(n)

    heap = [n for n in nodes if indegree[n] == 0]
    heapq.heapify(heap)
    result = []
    while heap:
        n = heapq.heappop(heap)
        result.append(n)
        for m in dependents[n]:
            indegree[m] -= 1
            if indegree[m] == 0:
                heapq.heappush(heap, m)

    if len(result) != len(nodes):
        raise ValueError("cycle detected")
    return result
