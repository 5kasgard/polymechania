import datetime

def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    """
    Returns the number of business days (Mon-Fri) in [start, end).
    If end < start, returns negative count for [end, start).
    Efficiently handles large ranges.
    """
    if start == end:
        return 0

    if end < start:
        return -business_days(end, start, holidays)

    total_days = (end - start).days
    full_weeks = total_days // 7
    remaining_days = total_days % 7

    # Every full week has exactly 5 business days
    count = full_weeks * 5

    # Handle the remaining days in the partial week
    current_date = start + datetime.timedelta(days=full_weeks * 7)
    while current_date < end:
        # weekday() returns 0 for Monday, 6 for Sunday
        if current_date.weekday() < 5:
            count += 1
        current_date += datetime.timedelta(days=1)

    # Subtract holidays that are weekdays and fall within [start, end)
    for holiday in holidays:
        if start <= holiday < end:
            if holiday.weekday() < 5:
                count -= 1

    return count
