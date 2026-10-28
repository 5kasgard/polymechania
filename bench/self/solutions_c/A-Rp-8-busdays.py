import datetime


def _weekdays_before(ordinal: int) -> int:
    # Number of weekdays (Mon-Fri) with ordinal in [1, ordinal).
    # date.toordinal(): 0001-01-01 is ordinal 1 and is a Monday.
    n = ordinal - 1  # days in [1, ordinal)
    full_weeks, rem = divmod(n, 7)
    # Each full week contributes 5 weekdays. The remaining `rem` days
    # start on a Monday, so they contribute min(rem, 5) weekdays.
    return full_weeks * 5 + min(rem, 5)


def _count_weekdays(start: datetime.date, end: datetime.date) -> int:
    # Weekdays d with start <= d < end, assuming start <= end.
    return _weekdays_before(end.toordinal()) - _weekdays_before(start.toordinal())


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)

    total = _count_weekdays(start, end)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            total -= 1
    return total
