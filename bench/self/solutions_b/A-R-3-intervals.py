def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not xs:
        return []

    # Sort by start point to allow single-pass merging
    sorted_intervals = sorted(xs)
    
    merged: list[tuple[int, int]] = []
    
    for current in sorted_intervals:
        if not merged:
            merged.append(current)
            continue
        
        last_start, last_end = merged[-1]
        curr_start, curr_end = current
        
        # If the current interval starts before or exactly when the last one ends, they merge
        if curr_start <= last_end:
            # Update the last interval in the list with the new maximum end point
            merged[-1] = (last_start, max(last_end, curr_end))
        else:
            # No overlap or touch, add as a new interval
            merged.append(current)
            
    return merged
