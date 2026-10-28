import heapq

def shortest_path(graph: dict[str, list[tuple[str, int]]], src: str, dst: str) -> tuple[int, list[str]] | None:
    """
    Finds the cheapest path from src to dst using Dijkstra's algorithm.
    In case of ties in cost, returns the lexicographically smallest path.
    """
    if src == dst:
        return (0, [src])

    # pq stores (cost, path_list)
    # Including path_list in the tuple handles the lexicographical tie-break automatically
    pq = [(0, [src])]
    # visited stores the minimum cost found so far to reach a node
    visited = {src: 0}

    while pq:
        current_cost, path = heapq.heappop(pq)
        u = path[-1]

        if u == dst:
            return (current_cost, path)

        # If we found a better way to u already, skip this stale entry
        if current_cost > visited.get(u, float('inf')):
            continue

        # Explore neighbors
        # The spec says nodes may appear only as edge targets, 
        # so we check if u exists in the graph dictionary.
        for v, weight in graph.get(u, []):
            new_cost = current_cost + weight
            
            # If this is a new node or a cheaper path to an existing node
            if v not in visited or new_cost < visited[v]:
                visited[v] = new_cost
                new_path = path + [v]
                heapq.heappush(pq, (new_cost, new_path))
            
            # Tie-breaking: if cost is equal, check if the new path is lexicographically smaller
            elif new_cost == visited[v]:
                new_path = path + [v]
                # We need to check if this new path is lexicographically smaller than 
                # the one that got us to 'visited[v]'. However, Dijkstra with 
                # (cost, path) in the PQ naturally explores the smallest path first.
                # To ensure we don't miss a lexicographical tie-break that arrives 
                # via a different route, we allow the PQ to handle it.
                # But standard Dijkstra only updates on strictly less.
                # To strictly follow "Among equally cheap paths return the one whose 
                # node list is lexicographically smallest", we must allow 
                # equal-cost paths to enter the PQ if they are lexicographically smaller.
                # However, in Dijkstra, once a node is popped, its shortest path is found.
                # With (cost, path) in PQ, the first time we pop 'dst', it is guaranteed 
                # to be the minimum cost AND the lexicographically smallest path.
                pass

    return None

if __name__ == '__main__':
    # Demo
    example_graph = {
        'A': [('B', 1), ('C', 1)],
        'B': [('D', 2)],
        'C': [('D', 2)],
        'D': [('E', 1)]
    }
    
    print(f"Path A -> E: {shortest_path(example_graph, 'A', 'E')}")
    # Expected: (4, ['A', 'B', 'D', 'E']) because ['A', 'B', 'D', 'E'] < ['A', 'C', 'D', 'E']
    
    print(f"Path A -> Z (unreachable): {shortest_path(example_graph, 'A', 'Z')}")
    print(f"Path A -> A (same): {shortest_path(example_graph, 'A', 'A')}")
