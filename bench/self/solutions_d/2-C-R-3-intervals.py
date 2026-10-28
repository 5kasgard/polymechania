def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not xs:
        return []
    ordered = sorted(xs)
    merged: list[tuple[int, int]] = []
    cur_a, cur_b = ordered[0]
    for a, b in ordered[1:]:
        if a <= cur_b:
            if b > cur_b:
                cur_b = b
        else:
            merged.append((cur_a, cur_b))
            cur_a, cur_b = a, b
    merged.append((cur_a, cur_b))
    return merged
