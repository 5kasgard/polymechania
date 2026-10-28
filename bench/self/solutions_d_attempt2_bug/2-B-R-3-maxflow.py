# NOTE: specification for order 3 was missing (text was only "r"); this is a
# best-guess Edmonds-Karp max-flow over a capacity matrix, to be revised.
from collections import deque


def maxflow(capacity, source, sink):
    n = len(capacity)
    residual = [list(row) for row in capacity]
    flow = 0
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
            return flow
        bottleneck = None
        v = sink
        while v != source:
            u = parent[v]
            if bottleneck is None or residual[u][v] < bottleneck:
                bottleneck = residual[u][v]
            v = u
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck
            v = u
        flow += bottleneck
