import heapq

def shortest_path(graph: dict[str, list[tuple[str, int]]], src: str, dst: str) -> tuple[int, list[str]] | None:
    if src == dst:
        return (0, [src])

    # distances[node] = (cost, path_as_list)
    # We use the path in the heap/distance tracker to handle the lexicographical tie-breaking requirement.
    # Dijkstra's algorithm with a priority queue.
    # Priority queue stores: (cost, path)
    # Because we want the lexicographically smallest path among equal costs, 
    # and tuples in Python are compared element by element, (cost, path) 
    # works perfectly for the priority queue.
    
    pq = [(0, [src])]
    visited = {}  # node -> (cost, path)

    while pq:
        cost, path = heapq.heappop(pq)
        u = path[-1]

        if u in visited:
            prev_cost, prev_path = visited[u]
            if cost > prev_cost:
                continue
            if cost == prev_cost and path >= prev_path:
                continue
        
        visited[u] = (cost, path)

        if u == dst:
            return (cost, path)

        if u in graph:
            for v, weight in graph[u]:
                new_cost = cost + weight
                new_path = path + [v]
                
                if v not in visited or new_cost < visited[v][0] or (new_cost == visited[v][0] and new_path < visited[v][1]):
                    heapq.heappush(pq, (new_cost, new_path))

    return None

if __name__ == '__main__':
    # Demo
    g = {
        'A': [('B', 1), ('C', 2)],
        'B': [('D', 2), ('C', 1)],
        'C': [('D', 1)],
        'D': []
    }
    # Path A->B->C->D cost 3, path ['A', 'B', 'C', 'D']
    # Path A->C->D cost 3, path ['A', 'C', 'D']
    # Lexicographically ['A', 'B', 'C', 'D'] < ['A', 'C', 'D']
    print(f"Shortest path A to D: {shortest_path(g, 'A', 'D')}")
    
    g2 = {
        'A': [('B', 10), ('C', 10)],
        'B': [('D', 10)],
        'C': [('D', 10)]
    }
    # Both paths cost 20. ['A', 'B', 'D'] vs ['A', 'C', 'D']
    print(f"Tie-break A to D: {shortest_path(g2, 'A', 'D')}")
    
    print(f"Unreachable: {shortest_path(g, 'A', 'E')}")
    print(f"Same node: {shortest_path(g, 'A', 'A')}")
