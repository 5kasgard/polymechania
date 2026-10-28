POP = [bin(m).count("1") for m in range(512)]


def sudoku(grid: str) -> str | None:
    if len(grid) != 81:
        return None

    ROW = [i // 9 for i in range(81)]
    COL = [i % 9 for i in range(81)]
    BOX = [(i // 27) * 3 + (i % 9) // 3 for i in range(81)]

    vals = [0] * 81
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9

    for i, ch in enumerate(grid):
        if ch in "123456789":
            d = int(ch)
            bit = 1 << (d - 1)
            r, c, b = ROW[i], COL[i], BOX[i]
            if (rows[r] | cols[c] | boxes[b]) & bit:
                return None
            vals[i] = d
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit

    empties = [i for i in range(81) if vals[i] == 0]

    def search(empties):
        if not empties:
            return True

        best_idx = -1
        best_mask = 0
        best_cnt = 10
        for idx in empties:
            r, c, b = ROW[idx], COL[idx], BOX[idx]
            mask = ~(rows[r] | cols[c] | boxes[b]) & 511
            cnt = POP[mask]
            if cnt == 0:
                return False
            if cnt < best_cnt:
                best_cnt = cnt
                best_idx = idx
                best_mask = mask
                if cnt == 1:
                    break

        idx = best_idx
        r, c, b = ROW[idx], COL[idx], BOX[idx]
        rest = [e for e in empties if e != idx]
        m = best_mask
        while m:
            low = m & -m
            m ^= low
            bit = low
            vals[idx] = low.bit_length()
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            if search(rest):
                return True
            rows[r] ^= bit
            cols[c] ^= bit
            boxes[b] ^= bit
            vals[idx] = 0
        return False

    if not search(empties):
        return None
    return "".join(str(v) for v in vals)
