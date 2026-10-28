import datetime


def _weekdays_before(d: datetime.date) -> int:
    # Number of weekdays in the half-open range [epoch, d) for a fixed
    # reference epoch, using ordinal arithmetic so it is O(1).
    # Reference: ordinal 1 (0001-01-01) is a Monday.
    n = d.toordinal() - 1  # days elapsed since 0001-01-01 (a Monday)
    weeks, rem = divmod(n, 7)
    return weeks * 5 + min(rem, 5)


def _count_range(start: datetime.date, end: datetime.date,
                 holidays: set[datetime.date]) -> int:
    # Count weekdays in [start, end) not in holidays, assuming start <= end.
    total = _weekdays_before(end) - _weekdays_before(start)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            total -= 1
    return total


def business_days(start: datetime.date, end: datetime.date,
                  holidays: set[datetime.date]) -> int:
    if end < start:
        return -_count_range(end, start, holidays)
    return _count_range(start, end, holidays)
