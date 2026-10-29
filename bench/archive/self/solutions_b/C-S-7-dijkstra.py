import heapq

def shortest_path(graph: dict[str, list[tuple[str, int]]], src: str, dst: str):
    """
    Finds the cheapest path from src to dst using Dijkstra's algorithm.
    Ties are broken by the lexicographically smallest path.
    """
    if src == dst:
        return (0, [src])

    # Priority queue stores (cost, path)
    # heapq will compare cost first, then the path list for tie-breaking
    pq = [(0, [src])]
    
    # visited stores the minimum cost found so far for a node
    # to allow for path tie-breaking, we also need to track the best path
    # but Dijkstra's with (cost, path) in PQ handles this naturally.
    # However, we need to avoid re-processing nodes with higher costs.
    best_costs = {src: 0}

    while pq:
        current_cost, path = heapq.heappop(pq)
        u = path[-1]

        if u == dst:
            return (current_cost, path)

        # If we found a better way to u already, skip
        if current_cost > best_costs.get(u, float('inf')):
            continue

        # Explore neighbors
        # Note: graph might not contain u if u has no outgoing edges
        for v, weight in graph.get(u, []):
            new_cost = current_cost + weight
            new_path = path + [v]

            if v not in best_costs or new_cost < best_costs[v]:
                best_costs[v] = new_cost
                heapq.heappush(pq, (new_cost, new_path))
            elif new_cost == best_costs[v]:
                # If cost is equal, check if the new path is lexicographically smaller
                # This is important for the tie-breaking rule.
                # We need to check if this new path is better than the one that 
                # resulted in best_costs[v]. Since we don't store the best path 
                # in best_costs, we rely on the PQ to eventually pop the best one.
                # To be safe and efficient, we can push it anyway; the PQ handles it.
                heapq.heappush(pq, (new_cost, new_path))

    return None

if __name__ == '__main__':
    # Demo 1: Standard path
    g1 = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
    }
    print(f"Demo 1: {shortest_path(g1, 'A', 'D')}")  # Expected: (4, ['A', 'B', 'C', 'D'])

    # Demo 2: Tie-breaking (lexicographical)
    # Path A-B-D is (2, ['A', 'B', 'D'])
    # Path A-C-D is (2, ['A', 'C', 'D'])
    # ['A', 'B', 'D'] < ['A', 'C', 'D']
    g2 = {
        'A': [('B', 1), ('C', 1)],
        'B': [('D', 1)],
        'C': [('D', 1)],
    }
    print(f"Demo 2: {shortest_path(g2, 'A', 'D')}")  # Expected: (2, ['A', 'B', 'D'])

    # Demo 3: Unreachable
    g3 = {'A': [('B', 1)]}
    print(f"Demo 3: {shortest_path(g3, 'A', 'C')}")  # Expected: None

    # Demo 4: Start is destination
    print(f"Demo 4: {shortest_path(g1, 'A', 'A')}")  # Expected: (0, ['A'])
