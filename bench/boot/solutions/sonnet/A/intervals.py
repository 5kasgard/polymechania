def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    result = []
    for a, b in sorted(xs):
        if result and a <= result[-1][1]:
            if b > result[-1][1]:
                result[-1] = (result[-1][0], b)
        else:
            result.append((a, b))
    return result
