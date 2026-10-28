def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not xs:
        return []
    ordered = sorted(xs)
    merged = [list(ordered[0])]
    for a, b in ordered[1:]:
        if a <= merged[-1][1]:
            if b > merged[-1][1]:
                merged[-1][1] = b
        else:
            merged.append([a, b])
    return [(a, b) for a, b in merged]
