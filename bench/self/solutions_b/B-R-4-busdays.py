import datetime

def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    """
    Returns the number of days d with start <= d < end that are Monday to Friday 
    and not in holidays. If end < start, return minus the count for the range [end, start).
    """
    if start == end:
        return 0

    is_negative = False
    if end < start:
        is_negative = True
        start, end = end, start

    # Total days in range [start, end)
    total_days = (end - start).days
    
    # Calculate full weeks and remaining days
    full_weeks = total_days // 7
    remaining_days = total_days % 7
    
    # Each full week has exactly 5 business days
    count = full_weeks * 5
    
    # Handle the remaining days
    # start_weekday: 0=Mon, 1=Tue, ..., 5=Sat, 6=Sun
    current_day_offset = 0
    start_weekday = start.weekday()
    
    while current_day_offset < remaining_days:
        weekday = (start_weekday + current_day_offset) % 7
        if weekday < 5:  # Monday to Friday
            count += 1
        current_day_offset += 1

    # Subtract holidays that fall within [start, end) and are Mon-Fri
    # We only care about holidays that are actually in the range and are weekdays
    for holiday in holidays:
        if start <= holiday < end:
            if holiday.weekday() < 5:
                count -= 1

    return -count if is_negative else count
