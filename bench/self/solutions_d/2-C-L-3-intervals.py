def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not xs:
        return []
    ordered = sorted(xs)
    merged = []
    cur_start, cur_end = ordered[0]
    for start, end in ordered[1:]:
        if start <= cur_end:
            if end > cur_end:
                cur_end = end
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = start, end
    merged.append((cur_start, cur_end))
    return merged
