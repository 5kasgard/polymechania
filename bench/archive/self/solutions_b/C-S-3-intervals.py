def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not xs:
        return []

    # Sort intervals by start point
    sorted_intervals = sorted(xs)

    merged = []
    # Initialize with the first interval
    current_start, current_end = sorted_intervals[0]

    for i in range(1, len(sorted_intervals)):
        next_start, next_end = sorted_intervals[i]

        # If the next interval starts before or exactly when the current one ends, they overlap or touch
        if next_start <= current_end:
            # Merge by extending the end point if the next interval goes further
            current_end = max(current_end, next_end)
        else:
            # No overlap, push the completed interval and move to the next
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end

    # Append the final interval
    merged.append((current_start, current_end))

    return merged
