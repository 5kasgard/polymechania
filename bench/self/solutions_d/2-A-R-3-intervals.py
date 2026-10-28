def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not xs:
        return []
    items = sorted(xs)
    merged: list[tuple[int, int]] = []
    cur_start, cur_end = items[0]
    for a, b in items[1:]:
        if a <= cur_end:
            if b > cur_end:
                cur_end = b
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = a, b
    merged.append((cur_start, cur_end))
    return merged
