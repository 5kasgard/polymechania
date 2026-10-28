def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    for a, b in sorted(xs):
        if result and a <= result[-1][1]:
            last_a, last_b = result[-1]
            result[-1] = (last_a, max(last_b, b))
        else:
            result.append((a, b))
    return result
