def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not xs:
        return []
    ordered = sorted(xs)
    merged = [ordered[0]]
    for a, b in ordered[1:]:
        last_a, last_b = merged[-1]
        if a <= last_b:
            merged[-1] = (last_a, max(last_b, b))
        else:
            merged.append((a, b))
    return merged
