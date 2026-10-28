def sudoku(grid: str) -> str | None:
    if len(grid) != 81:
        return None
    cells = [0] * 81
    for i, ch in enumerate(grid):
        if ch == ".":
            cells[i] = 0
        elif ch in "123456789":
            cells[i] = int(ch)
        else:
            return None

    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9

    def box_of(r, c):
        return (r // 3) * 3 + c // 3

    for i, v in enumerate(cells):
        if v:
            r, c = divmod(i, 9)
            b = box_of(r, c)
            bit = 1 << v
            if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                return None
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit

    empties = [i for i in range(81) if cells[i] == 0]

    def candidates(i):
        r, c = divmod(i, 9)
        used = rows[r] | cols[c] | boxes[box_of(r, c)]
        return [v for v in range(1, 10) if not used & (1 << v)]

    def place(i, v):
        r, c = divmod(i, 9)
        bit = 1 << v
        rows[r] |= bit
        cols[c] |= bit
        boxes[box_of(r, c)] |= bit
        cells[i] = v

    def remove(i, v):
        r, c = divmod(i, 9)
        bit = 1 << v
        rows[r] &= ~bit
        cols[c] &= ~bit
        boxes[box_of(r, c)] &= ~bit
        cells[i] = 0

    def solve(remaining):
        if not remaining:
            return True
        # Pick the empty cell with the fewest candidates (MRV heuristic).
        best_idx = -1
        best_cands = None
        for k, i in enumerate(remaining):
            cands = candidates(i)
            if best_cands is None or len(cands) < len(best_cands):
                best_idx, best_cands = k, cands
                if len(cands) <= 1:
                    break
        if not best_cands:
            return False
        i = remaining[best_idx]
        rest = remaining[:best_idx] + remaining[best_idx + 1:]
        for v in best_cands:
            place(i, v)
            if solve(rest):
                return True
            remove(i, v)
        return False

    if not solve(empties):
        return None
    return "".join(str(v) for v in cells)
