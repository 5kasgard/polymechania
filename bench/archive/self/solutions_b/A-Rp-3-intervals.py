def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not xs:
        return []

    # Sort by start point, then end point
    sorted_xs = sorted(xs)

    merged = []
    curr_start, curr_end = sorted_xs[0]

    for i in range(1, len(sorted_xs)):
        next_start, next_end = sorted_xs[i]

        # If the next interval starts before or exactly when the current one ends
        if next_start <= curr_end:
            # Merge by extending the end point
            curr_end = max(curr_end, next_end)
        else:
            # No overlap or touch, push the completed interval
            merged.append((curr_start, curr_end))
            curr_start, curr_end = next_start, next_end

    # Add the final interval
    merged.append((curr_start, curr_end))

    return merged
