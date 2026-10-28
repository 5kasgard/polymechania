# NOTE: specification was only "r"; this is a best-effort Edmonds-Karp
# max-flow over a capacity matrix, to be revised once the real spec arrives.
from collections import deque


def maxflow(capacity, source, sink):
    n = len(capacity)
    residual = [list(row) for row in capacity]
    total = 0
    while True:
        parent = [-1] * n
        parent[source] = source
        queue = deque([source])
        while queue and parent[sink] == -1:
            u = queue.popleft()
            for v in range(n):
                if parent[v] == -1 and residual[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if parent[sink] == -1:
            return total
        bottleneck = None
        v = sink
        while v != source:
            u = parent[v]
            cap = residual[u][v]
            bottleneck = cap if bottleneck is None else min(bottleneck, cap)
            v = u
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck
            v = u
        total += bottleneck
