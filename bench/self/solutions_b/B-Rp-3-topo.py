import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # Identify all nodes
    all_nodes = set(deps.keys())
    for neighbors in deps.values():
        for n in neighbors:
            all_nodes.add(n)
    
    # Build adjacency list (dependency -> dependent) and in-degree count
    # The input 'deps' is: node -> list of things it depends on
    # We need: dependency -> list of nodes that depend on it
    adj = {node: [] for node in all_nodes}
    in_degree = {node: 0 for node in all_nodes}
    
    for node, dependencies in deps.items():
        for d in dependencies:
            adj[d].append(node)
            in_degree[node] += 1
            
    # Kahn's algorithm with a min-heap for lexicographical order
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
