def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merges closed intervals that overlap or touch.
    Returns a list of merged intervals sorted by start.
    """
    if not xs:
        return []

    # Sort intervals by start point
    sorted_intervals = sorted(xs)

    merged: list[tuple[int, int]] = []
    
    for current in sorted_intervals:
        # If merged is empty, or the current interval does not overlap/touch 
        # the last merged interval, add it.
        if not merged or current[0] > merged[-1][1]:
            merged.append(current)
        else:
            # There is an overlap or they touch (current[0] <= merged[-1][1]).
            # Merge by updating the end of the last interval in 'merged'.
            last_start, last_end = merged[-1]
            merged[-1] = (last_start, max(last_end, current[1]))

    return merged
