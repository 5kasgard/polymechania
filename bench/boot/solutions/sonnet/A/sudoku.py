def sudoku(grid):
    if not isinstance(grid, str) or len(grid) != 81:
        return None

    rows = [[r * 9 + c for c in range(9)] for r in range(9)]
    cols = [[r * 9 + c for r in range(9)] for c in range(9)]
    boxes = [[(br * 3 + r) * 9 + bc * 3 + c for r in range(3) for c in range(3)]
             for br in range(3) for bc in range(3)]
    units = rows + cols + boxes
    units_of = [[] for _ in range(81)]
    for u in units:
        for s in u:
            units_of[s].append(u)
    peers = []
    for s in range(81):
        p = set()
        for u in units_of[s]:
            p.update(u)
        p.discard(s)
        peers.append(sorted(p))

    pop = [bin(i).count("1") for i in range(512)]

    def eliminate(cand, s0, m0):
        stack = [(s0, m0)]
        while stack:
            s, m = stack.pop()
            removed = cand[s] & m
            if not removed:
                continue
            c = cand[s] & ~m
            cand[s] = c
            if c == 0:
                return False
            if c & (c - 1) == 0:
                for p in peers[s]:
                    if cand[p] & c:
                        stack.append((p, c))
            b = removed
            while b:
                low = b & -b
                b ^= low
                for u in units_of[s]:
                    count = 0
                    last = -1
                    for t in u:
                        if cand[t] & low:
                            count += 1
                            last = t
                            if count > 1:
                                break
                    if count == 0:
                        return False
                    if count == 1:
                        rest = cand[last] & ~low
                        if rest:
                            stack.append((last, rest))
        return True

    cand = [511] * 81
    for i, ch in enumerate(grid):
        if ch == ".":
            continue
        if ch not in "123456789":
            return None
        bit = 1 << (int(ch) - 1)
        if not cand[i] & bit:
            return None
        if not eliminate(cand, i, 511 & ~bit):
            return None

    def search(cand):
        best = -1
        bn = 10
        for i in range(81):
            n = pop[cand[i]]
            if n == 0:
                return None
            if 1 < n < bn:
                bn = n
                best = i
                if n == 2:
                    break
        if best < 0:
            return cand
        c = cand[best]
        while c:
            low = c & -c
            c ^= low
            new = cand[:]
            if eliminate(new, best, new[best] & ~low):
                res = search(new)
                if res is not None:
                    return res
        return None

    res = search(cand)
    if res is None:
        return None
    return "".join(str(x.bit_length()) for x in res)
