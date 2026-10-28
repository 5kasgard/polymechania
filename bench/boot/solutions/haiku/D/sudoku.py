def sudoku(grid: str) -> str | None:
    if len(grid) != 81:
        return None

    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    board = [0] * 81

    def box_of(r, c):
        return (r // 3) * 3 + (c // 3)

    for i, ch in enumerate(grid):
        if ch == ".":
            continue
        if ch < "1" or ch > "9":
            return None
        d = int(ch)
        r, c = divmod(i, 9)
        b = box_of(r, c)
        if d in rows[r] or d in cols[c] or d in boxes[b]:
            return None
        rows[r].add(d)
        cols[c].add(d)
        boxes[b].add(d)
        board[i] = d

    def candidates(i):
        r, c = divmod(i, 9)
        used = rows[r] | cols[c] | boxes[box_of(r, c)]
        return [d for d in range(1, 10) if d not in used]

    def place(i, d):
        r, c = divmod(i, 9)
        b = box_of(r, c)
        rows[r].add(d)
        cols[c].add(d)
        boxes[b].add(d)
        board[i] = d

    def remove(i, d):
        r, c = divmod(i, 9)
        b = box_of(r, c)
        rows[r].discard(d)
        cols[c].discard(d)
        boxes[b].discard(d)
        board[i] = 0

    # Iterative DFS with minimum-remaining-values heuristic.
    # Each stack frame: (cell index, list of remaining candidates) or None.
    def find_best_cell():
        best_i = -1
        best_cands = None
        best_len = 10
        for i in range(81):
            if board[i] != 0:
                continue
            cands = candidates(i)
            n = len(cands)
            if n < best_len:
                best_len = n
                best_i = i
                best_cands = cands
                if n <= 1:
                    break
        return best_i, best_cands

    # Stack of (cell, candidates, next_index)
    stack = []
    i, cands = find_best_cell()
    if i == -1:
        return "".join(str(d) for d in board)
    if not cands:
        return None
    stack.append([i, cands, 0])

    while stack:
        frame = stack[-1]
        cell, cands, k = frame
        # Undo previous placement at this frame, if any.
        if board[cell] != 0:
            remove(cell, board[cell])
        if k >= len(cands):
            stack.pop()
            continue
        d = cands[k]
        frame[2] = k + 1
        place(cell, d)
        ni, ncands = find_best_cell()
        if ni == -1:
            return "".join(str(x) for x in board)
        if ncands:
            stack.append([ni, ncands, 0])
        # If no candidates, loop continues and tries next value for this cell.

    return None
