import datetime

def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if start == end:
        return 0
    
    negate = False
    if end < start:
        start, end = end, start
        negate = True
    
    total_days = (end - start).days
    full_weeks = total_days // 7
    remaining_days = total_days % 7
    
    # Each full week has 5 weekdays
    count = full_weeks * 5
    
    # Check the remaining days
    current_date = start + datetime.timedelta(days=full_weeks * 7)
    for _ in range(remaining_days):
        if current_date.weekday() < 5:  # 0-4 is Mon-Fri
            count += 1
        current_date += datetime.timedelta(days=1)
        
    # Subtract holidays that are weekdays and within [start, end)
    weekday_holidays = 0
    for h in holidays:
        if start <= h < end:
            if h.weekday() < 5:
                weekday_holidays += 1
                
    result = count - weekday_holidays
    return -result if negate else result
