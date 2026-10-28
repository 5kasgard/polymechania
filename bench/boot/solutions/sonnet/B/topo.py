import heapq


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set()
    for n, ds in deps.items():
        nodes.add(n)
        for d in ds:
            nodes.add(d)

    # Unique dependency sets (duplicates must not inflate counts)
    dep_sets = {n: set() for n in nodes}
    for n, ds in deps.items():
        dep_sets[n].update(ds)

    dependents = {n: [] for n in nodes}
    indeg = {}
    for n, s in dep_sets.items():
        indeg[n] = len(s)
        for d in s:
            dependents[d].append(n)

    heap = [n for n, c in indeg.items() if c == 0]
    heapq.heapify(heap)
    result = []
    while heap:
        n = heapq.heappop(heap)
        result.append(n)
        for m in dependents[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                heapq.heappush(heap, m)

    if len(result) != len(nodes):
        raise ValueError("cycle detected")
    return result
