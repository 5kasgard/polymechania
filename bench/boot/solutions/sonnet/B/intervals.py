def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not xs:
        return []
    items = sorted(xs)
    result = []
    cur_a, cur_b = items[0]
    for a, b in items[1:]:
        if a <= cur_b:
            if b > cur_b:
                cur_b = b
        else:
            result.append((cur_a, cur_b))
            cur_a, cur_b = a, b
    result.append((cur_a, cur_b))
    return result
