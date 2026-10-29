import heapq

def shortest_path(graph: dict[str, list[tuple[str, int]]], src: str, dst: str) -> tuple[int, list[str]] | None:
    """
    Finds the cheapest path from src to dst using Dijkstra's algorithm.
    Ties in cost are broken by the lexicographically smallest path.
    """
    if src == dst:
        return (0, [src])

    # pq stores (cost, path_as_list)
    # Using the path itself in the heap allows lexicographical tie-breaking
    pq = [(0, [src])]
    # visited stores the minimum cost found so far to reach a node
    visited = {src: 0}

    while pq:
        current_cost, path = heapq.heappop(pq)
        u = path[-1]

        if u == dst:
            return (current_cost, path)

        # If we found a better way to u already, skip
        if current_cost > visited.get(u, float('inf')):
            continue

        # Check neighbors
        # The spec says nodes may appear only as edge targets, 
        # so we check if u is a key in the graph dict.
        for v, weight in graph.get(u, []):
            new_cost = current_cost + weight
            new_path = path + [v]

            if v not in visited or new_cost < visited[v]:
                visited[v] = new_cost
                heapq.heappush(pq, (new_cost, new_path))
            elif new_cost == visited[v]:
                # If cost is equal, we check if the new path is lexicographically smaller
                # This is handled by the heap if we push it, but we only push if it's 
                # actually a candidate for the 'best' path to v.
                # However, Dijkstra with path in heap is safer for lexicographical requirements.
                heapq.heappush(pq, (new_cost, new_path))

    return None

if __name__ == '__main__':
    # Quick demo
    example_graph = {
        'A': [('B', 1), ('C', 1)],
        'B': [('D', 2)],
        'C': [('D', 2)],
        'D': [('E', 1)],
    }
    
    # Test 1: Standard path
    print(f"Path A to E: {shortest_path(example_graph, 'A', 'E')}")
    
    # Test 2: Lexicographical tie-break
    # A -> B -> D (cost 3, path ['A', 'B', 'D'])
    # A -> C -> D (cost 3, path ['A', 'C', 'D'])
    # ['A', 'B', 'D'] is lexicographically smaller than ['A', 'C', 'D']
    print(f"Tie-break A to D: {shortest_path(example_graph, 'A', 'D')}")
    
    # Test 3: Unreachable
    print(f"Unreachable: {shortest_path(example_graph, 'E', 'A')}")
    
    # Test 4: src == dst
    print(f"Same node: {shortest_path(example_graph, 'A', 'A')}")
