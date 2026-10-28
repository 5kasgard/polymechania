import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # Identify all nodes
    all_nodes = set(deps.keys())
    for neighbors in deps.values():
        for node in neighbors:
            all_nodes.add(node)
    
    # Build adjacency list (u -> v means v depends on u)
    # and calculate in-degrees
    adj = {node: [] for node in all_nodes}
    in_degree = {node: 0 for node in all_nodes}
    
    for node, dependencies in deps.items():
        for dep in dependencies:
            # dep must come before node
            # edge: dep -> node
            adj[dep].append(node)
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
