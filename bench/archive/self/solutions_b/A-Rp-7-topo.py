import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    """
    Performs a topological sort on a dependency graph.
    Returns nodes in an order where dependencies come before the nodes that depend on them.
    Ties are broken by selecting the alphabetically smallest node first.
    Raises ValueError if a cycle is detected.
    """
    # 1. Identify all unique nodes and build the graph
    # adj: node -> list of nodes that depend on it
    # in_degree: node -> number of dependencies it has
    adj = {}
    in_degree = {}
    
    # Initialize all nodes mentioned in keys or values
    all_nodes = set(deps.keys())
    for dependencies in deps.values():
        for d in dependencies:
            all_nodes.add(d)
            
    for node in all_nodes:
        adj[node] = []
        in_degree[node] = 0
        
    # 2. Populate the adjacency list and in-degree counts
    for node, dependencies in deps.items():
        for d in dependencies:
            # d must come before node
            adj[d].append(node)
            in_degree[node] += 1
            
    # 3. Kahn's algorithm using a min-heap for lexicographical order
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
                
    # 4. Check for cycles
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected in dependencies")
        
    return result

if __name__ == '__main__':
    # Demo 1: Standard DAG
    example1 = {
        'B': ['A'],
        'C': ['A'],
        'D': ['B', 'C']
    }
    print(f"Order 1: {topo_sort(example1)}")  # Expected: ['A', 'B', 'C', 'D']

    # Demo 2: Tie-breaking (alphabetical)
    example2 = {
        'C': ['A'],
        'B': ['A'],
        'D': []
    }
    print(f"Order 2: {topo_sort(example2)}")  # Expected: ['A', 'B', 'C', 'D'] or ['A', 'B', 'D', 'C']? 
    # Wait, if A is done, B, C, and D are all ready. Smallest is B, then C, then D.
    # Let's re-verify: A is done. B, C, D have in-degree 0. 
    # Heap: [B, C, D]. Pop B. Pop C. Pop D. Result: [A, B, C, D]

    # Demo 3: Cycle detection
    example3 = {
        'A': ['B'],
        'B': ['A']
    }
    try:
        print("Order 3: ", end="")
        topo_sort(example3)
    except ValueError as e:
        print(f"Caught expected error: {e}")
