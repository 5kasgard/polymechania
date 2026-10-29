import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. Identify all nodes
    all_nodes = set(deps.keys())
    for neighbors in deps.values():
        for n in neighbors:
            all_nodes.add(n)
    
    # 2. Build adjacency list (dependency -> nodes that depend on it)
    # and calculate in-degrees (number of dependencies for each node)
    adj = {node: [] for node in all_nodes}
    in_degree = {node: 0 for node in all_nodes}
    
    for node, dependencies in deps.items():
        in_degree[node] = len(dependencies)
        for dep in dependencies:
            adj[dep].append(node)
            
    # 3. Kahn's algorithm with a min-priority queue
    # The priority queue stores nodes with in-degree 0
    queue = [node for node in all_nodes if in_degree[node] == 0]
    heapq.heapify(queue)
    
    sorted_list = []
    
    while queue:
        u = heapq.heappop(queue)
        sorted_list.append(u)
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(queue, v)
                
    # 4. Check for cycles
    if len(sorted_list) != len(all_nodes):
        raise ValueError("Cycle detected in dependencies")
        
    return sorted_list
