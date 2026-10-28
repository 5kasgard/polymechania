def merge_intervals(xs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not xs:
        return []

    # Sort by start point, then end point
    sorted_xs = sorted(xs)
    
    merged: list[tuple[int, int]] = []
    
    for start, end in sorted_xs:
        if not merged:
            merged.append((start, end))
            continue
        
        last_start, last_end = merged[-1]
        
        # If the current interval overlaps or touches the last one
        if start <= last_end:
            # Merge by updating the end of the last interval in the list
            new_end = max(last_end, end)
            merged[-1] = (last_start, new_end)
        else:
            # No overlap or touch, add as a new interval
            merged.append((start, end))
            
    return merged
