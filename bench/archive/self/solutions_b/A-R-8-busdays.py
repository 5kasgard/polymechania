import datetime

def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if start == end:
        return 0
    
    if end < start:
        return -business_days(end, start, holidays)

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
        
    # Subtract holidays that fall on a weekday within [start, end)
    # We only care about holidays that are actually in the range and are Mon-Fri
    for holiday in holidays:
        if start <= holiday < end:
            if holiday.weekday() < 5:
                count -= 1
                
    return count
