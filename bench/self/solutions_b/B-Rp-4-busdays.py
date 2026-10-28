import datetime

def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if start == end:
        return 0
    
    if end < start:
        return -business_days(end, start, holidays)
    
    # Total days in range [start, end)
    total_days = (end - start).days
    full_weeks = total_days // 7
    remaining_days = total_days % 7
    
    # Every full week has exactly 5 business days
    count = full_weeks * 5
    
    # Handle the remaining days
    current_date = start + datetime.timedelta(days=full_weeks * 7)
    for _ in range(remaining_days):
        if current_date.weekday() < 5:  # 0-4 is Mon-Fri
            count += 1
        current_date += datetime.timedelta(days=1)
        
    # Subtract holidays that are weekdays and within [start, end)
    # We only iterate over holidays, which is efficient for few holidays
    for h in holidays:
        if start <= h < end:
            if h.weekday() < 5:
                count -= 1
                
    return count
