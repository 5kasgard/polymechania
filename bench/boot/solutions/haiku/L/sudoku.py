# NOTE: none; solved by bitmask constraint search with minimum-remaining-values branching.

FULL = 0x1FF
_ROW = [i // 9 for i in range(81)]
_COL = [i % 9 for i in range(81)]
_BOX = [(i // 27) * 3 + (i % 9) // 3 for i in range(81)]


def sudoku(grid: str) -> str | None:
    if not isinstance(grid, str) or len(grid) != 81:
        return None

    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    board = [0] * 81

    for i, ch in enumerate(grid):
        if ch == '.':
            continue
        if ch not in '123456789':
            return None
        bit = 1 << (int(ch) - 1)
        r, c, b = _ROW[i], _COL[i], _BOX[i]
        if (rows[r] | cols[c] | boxes[b]) & bit:
            return None
        rows[r] |= bit
        cols[c] |= bit
        boxes[b] |= bit
        board[i] = int(ch)

    empties = [i for i in range(81) if board[i] == 0]

    def search() -> bool:
        if not empties:
            return True
        best_idx = -1
        best_cand = 0
        best_cnt = 10
        for k, i in enumerate(empties):
            r, c, b = _ROW[i], _COL[i], _BOX[i]
            cand = FULL & ~(rows[r] | cols[c] | boxes[b])
            cnt = bin(cand).count('1')
            if cnt < best_cnt:
                best_cnt = cnt
                best_idx = k
                best_cand = cand
                if cnt == 0:
                    return False
                if cnt == 1:
                    break
        i = empties[best_idx]
        r, c, b = _ROW[i], _COL[i], _BOX[i]
        last = empties.pop(best_idx)
        cand = best_cand
        while cand:
            bit = cand & -cand
            cand ^= bit
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            board[i] = bit.bit_length()
            if search():
                return True
            rows[r] ^= bit
            cols[c] ^= bit
            boxes[b] ^= bit
            board[i] = 0
        empties.insert(best_idx, last)
        return False

    if not search():
        return None
    return ''.join(str(d) for d in board)
