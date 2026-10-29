import datetime


def _weekdays_before(n: int) -> int:
    # Count of weekdays (Mon-Fri) among the first n days of a 7-day cycle
    # starting from a reference Monday (day offset 0 = Monday).
    full_weeks, rem = divmod(n, 7)
    return full_weeks * 5 + min(rem, 5)


def _count_weekdays_in_range(start: datetime.date, end: datetime.date) -> int:
    # Weekdays d with start <= d < end, assuming start <= end.
    ref = datetime.date(2000, 1, 3)  # a Monday
    a = (start - ref).days
    b = (end - ref).days
    return _weekdays_before(b) - _weekdays_before(a)


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)
    count = _count_weekdays_in_range(start, end)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            count -= 1
    return count
