import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    """
    Performs a topological sort on a dependency graph.
    Returns nodes in an order where dependencies come before the nodes.
    Ties are broken by alphabetical order.
    Raises ValueError if a cycle is detected.
    """
    # 1. Identify all unique nodes and build adjacency list (successors)
    # and in-degree counts.
    adj = {}
    in_degree = {}
    all_nodes = set(deps.keys())
    for predecessors in deps.values():
        for p in predecessors:
            all_nodes.add(p)
    
    for node in all_nodes:
        adj[node] = []
        in_degree[node] = 0
        
    # 2. Populate adjacency list and in-degrees
    # Note: deps[n] = [a, b] means a -> n and b -> n
    for node, predecessors in deps.items():
        for p in predecessors:
            adj[p].append(node)
            in_degree[node] += 1
            
    # 3. Kahn's algorithm with a min-heap for alphabetical tie-breaking
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
                
    # 4. Cycle detection
    if len(sorted_list) != len(all_nodes):
        raise ValueError("Cycle detected in dependency graph")
        
    return sorted_list
