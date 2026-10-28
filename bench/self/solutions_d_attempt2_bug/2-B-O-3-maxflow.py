from collections import deque, defaultdict


def maxflow(edges, source, sink):
    # NOTE: specification text was missing ("r"); signature assumed:
    # edges is an iterable of (u, v, capacity) with integer capacity >= 0.
    if source == sink:
        return 0

    cap = defaultdict(lambda: defaultdict(int))
    nodes = set()
    for u, v, c in edges:
        nodes.add(u)
        nodes.add(v)
        if u == v:
            continue
        cap[u][v] += c
        cap[v][u] += 0  # ensure reverse residual exists
    nodes.add(source)
    nodes.add(sink)

    flow = 0
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            x = queue.popleft()
            for y, c in cap[x].items():
                if c > 0 and y not in parent:
                    parent[y] = x
                    queue.append(y)
        if sink not in parent:
            break
        # find bottleneck
        bottleneck = None
        y = sink
        while parent[y] is not None:
            x = parent[y]
            r = cap[x][y]
            bottleneck = r if bottleneck is None else min(bottleneck, r)
            y = x
        # augment
        y = sink
        while parent[y] is not None:
            x = parent[y]
            cap[x][y] -= bottleneck
            cap[y][x] += bottleneck
            y = x
        flow += bottleneck

    return flow
