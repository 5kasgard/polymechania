import heapq

def shortest_path(graph: dict[str, list[tuple[str, int]]], src: str, dst: str) -> tuple[int, list[str]] | None:
    if src == dst:
        return (0, [src])

    # distances[node] = (cost, path_as_list)
    # We use the path in the heap/distance tracker to handle the lexicographical tie-breaking requirement.
    # Dijkstra's algorithm with a priority queue.
    # Priority queue stores: (cost, path)
    # Since we want the lexicographically smallest path for equal costs, 
    # and heapq compares tuples element by element, (cost, path) works perfectly.
    
    pq = [(0, [src])]
    visited = {}  # node -> (cost, path)

    while pq:
        current_cost, path = heapq.heappop(pq)
        u = path[-1]

        if u == dst:
            return (current_cost, path)

        if u in visited:
            prev_cost, prev_path = visited[u]
            if current_cost > prev_cost:
                continue
            if current_cost == prev_cost and path >= prev_path:
                continue
        
        visited[u] = (current_cost, path)

        if u in graph:
            for v, weight in graph[u]:
                new_cost = current_cost + weight
                new_path = path + [v]
                
                if v not in visited or (new_cost, new_path) < visited[v]:
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
    print(f"Test 1: {shortest_path(g, 'A', 'D')}") 
    
    g2 = {
        'A': [('B', 10), ('C', 10)],
        'B': [('D', 1)],
        'C': [('D', 1)]
    }
    # Both paths cost 11. ['A', 'B', 'D'] vs ['A', 'C', 'D'].
    print(f"Test 2: {shortest_path(g2, 'A', 'D')}")

    print(f"Test 3 (Unreachable): {shortest_path(g2, 'A', 'E')}")
    print(f"Test 4 (Same src/dst): {shortest_path(g2, 'A', 'A')}")
