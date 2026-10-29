import datetime

def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    """
    Returns the number of business days (Mon-Fri) d such that start <= d < end,
    excluding holidays. If end < start, returns -(business_days(end, start, holidays)).
    """
    if start == end:
        return 0
    
    if end < start:
        return -business_days(end, start, holidays)

    # Total days in the range [start, end)
    total_days = (end - start).days
    
    # Calculate full weeks and remaining days
    full_weeks = total_days // 7
    remaining_days = total_days % 7
    
    # Every full week has exactly 5 business days
    count = full_weeks * 5
    
    # Handle the remaining days after the full weeks
    # We iterate from start + (full_weeks * 7) up to end - 1
    current_date = start + datetime.timedelta(days=full_weeks * 7)
    while current_date < end:
        if current_date.weekday() < 5:  # 0-4 is Mon-Fri
            count += 1
        current_date += datetime.timedelta(days=1)
        
    # Subtract holidays that fall on a weekday within [start, end)
    # We only check holidays that are actually within the range to stay efficient
    for holiday in holidays:
        if start <= holiday < end:
            if holiday.weekday() < 5:
                count -= 1
                
    return count

if __name__ == '__main__':
    import datetime
    
    # Demo cases
    d1 = datetime.date(2023, 1, 2)  # Monday
    d2 = datetime.date(2023, 1, 9)  # Next Monday
    hols = {datetime.date(2023, 1, 4)} # Wednesday
    
    print(f"Range {d1} to {d2} with holiday {hols}:")
    print(f"Expected: 4, Got: {business_days(d1, d2, hols)}")
    
    d3 = datetime.date(2023, 1, 9)
    d4 = datetime.date(2023, 1, 2)
    print(f"Reverse range {d3} to {d4}:")
    print(f"Expected: -4, Got: {business_days(d3, d4, hols)}")
    
    # Large range test
    large_start = datetime.date(2000, 1, 1)
    large_end = datetime.date(3000, 1, 1)
    print(f"Large range (1000 years) count: {business_days(large_start, large_end, set())}")
