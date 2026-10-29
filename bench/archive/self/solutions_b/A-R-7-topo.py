import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    """
    Returns a topological sort of the nodes in deps.
    deps[n] is a list of nodes that n depends on.
    If multiple nodes are ready, the alphabetically smallest is chosen first.
    Raises ValueError if a cycle is detected.
    """
    # Build adjacency list (who depends on me) and in-degree count
    # nodes_to_process tracks all unique nodes mentioned
    adj = {}
    in_degree = {}
    all_nodes = set(deps.keys())
    for node, dependencies in deps.items():
        for d in dependencies:
            all_nodes.add(d)
    
    for node in all_nodes:
        adj[node] = []
        in_degree[node] = 0

    for node, dependencies in deps.items():
        for d in dependencies:
            # d must come before node. So d -> node
            adj[d].append(node)
            in_degree[node] += 1

    # Kahn's algorithm with a min-priority queue for alphabetical order
    queue = [node for node in all_nodes if in_degree[node] == 0]
    heapq.heapify(queue)
    
    result = []
    while queue:
        u = heapq.heappop(queue)
        result.append(u)
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(queue, v)
                
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected in dependencies")
        
    return result

if __name__ == '__main__':
    # Demo 1: Standard DAG
    # b depends on a; c depends on a; d depends on b and c
    d1 = {'b': ['a'], 'c': ['a'], 'd': ['b', 'c']}
    print(f"Order 1: {topo_sort(d1)}") # Expected: ['a', 'b', 'c', 'd'] or ['a', 'c', 'b', 'd']

    # Demo 2: Alphabetical tie-breaking
    # a and b are ready, a is smaller
    d2 = {'c': ['a', 'b'], 'b': [], 'a': []}
    print(f"Order 2: {topo_sort(d2)}") # Expected: ['a', 'b', 'c']

    # Demo 3: Cycle detection
    d3 = {'a': ['b'], 'b': ['a']}
    try:
        topo_sort(d3)
    except ValueError as e:
        print(f"Order 3: Caught expected error: {e}")

    # Demo 4: Disconnected components
    d4 = {'a': [], 'y': ['x'], 'x': []}
    print(f"Order 4: {topo_sort(d4)}") # Expected: ['a', 'x', 'y']
