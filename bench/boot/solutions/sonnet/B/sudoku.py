def sudoku(grid: str):
    if not isinstance(grid, str) or len(grid) != 81:
        raise ValueError("grid must be 81 characters")
    for ch in grid:
        if ch != "." and ch not in "123456789":
            raise ValueError("bad character")

    X = {j: set() for j in range(324)}
    Y = {}
    for r in range(9):
        for c in range(9):
            b = (r // 3) * 3 + c // 3
            for n in range(9):
                row = (r, c, n)
                Y[row] = [r * 9 + c, 81 + r * 9 + n, 162 + c * 9 + n, 243 + b * 9 + n]
                for j in Y[row]:
                    X[j].add(row)

    def select(r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols

    def deselect(r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)

    result = {}

    for idx, ch in enumerate(grid):
        if ch == ".":
            continue
        r, c = divmod(idx, 9)
        row = (r, c, int(ch) - 1)
        if any(j not in X for j in Y[row]):
            return None
        select(row)
        result[idx] = int(ch)

    sol = []

    def solve():
        if not X:
            return True
        best = None
        bl = 10
        for j, s in X.items():
            l = len(s)
            if l < bl:
                bl = l
                best = j
                if l <= 1:
                    break
        if bl == 0:
            return False
        for row in list(X[best]):
            sol.append(row)
            cols = select(row)
            if solve():
                return True
            deselect(row, cols)
            sol.pop()
        return False

    if not solve():
        return None
    for r, c, n in sol:
        result[r * 9 + c] = n + 1
    return "".join(str(result[i]) for i in range(81))
