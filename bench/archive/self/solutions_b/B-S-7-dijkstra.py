import heapq

def shortest_path(graph: dict[str, list[tuple[str, int]]], src: str, dst: str):
    if src == dst:
        return (0, [src])

    # dist[node] = (min_cost, min_path_list)
    # We use a dictionary to store the best known way to reach each node.
    best_visited = {src: (0, [src])}
    
    # Priority queue stores (cost, path, current_node)
    # Python's heapq will compare tuples element by element.
    # If costs are equal, it compares paths (lists of strings) lexicographically.
    pq = [(0, [src], src)]
    
    while pq:
        current_cost, path, u = heapq.heappop(pq)
        
        # If we found a better way to u already, skip this stale entry
        if current_cost > best_visited.get(u, (float('inf'), []))[0]:
            continue
        if current_cost == best_visited.get(u, (float('inf'), []))[0]:
            if path > best_visited.get(u, (float('inf'), []))[1]:
                continue

        # If we reached the destination, because it's a priority queue,
        # the first time we pop dst, it is guaranteed to be the cheapest.
        # Because the path is part of the tuple, it is also the lexicographically smallest.
        if u == dst:
            return (current_cost, path)

        # Explore neighbors
        # Note: nodes may appear only as edge targets, so we check if u is in graph
        for v, weight in graph.get(u, []):
            new_cost = current_cost + weight
            new_path = path + [v]
            
            if v not in best_visited or new_cost < best_visited[v][0]:
                best_visited[v] = (new_cost, new_path)
                heapq.heappush(pq, (new_cost, new_path, v))
            elif new_cost == best_visited[v][0]:
                if new_path < best_visited[v][1]:
                    best_visited[v] = (new_cost, new_path)
                    heapq.heappush(pq, (new_cost, new_path, v))
                    
    return None
