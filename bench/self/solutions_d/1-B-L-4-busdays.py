import datetime


def _weekdays_before(d: datetime.date) -> int:
    # Number of Mon-Fri days in the range [epoch, d), where epoch is a fixed Monday.
    # Using ordinal: date(1,1,1) is a Monday, so ordinal 0 corresponds to a Monday.
    n = d.toordinal() - 1  # days from 0001-01-01 (Monday) to d, exclusive of d
    weeks, rem = divmod(n, 7)
    # rem days into a week starting Monday: count weekdays among the first rem days
    return weeks * 5 + min(rem, 5)


def _count_range(start: datetime.date, end: datetime.date, holidays: set) -> int:
    # Assumes start <= end; counts weekdays d with start <= d < end not in holidays.
    total = _weekdays_before(end) - _weekdays_before(start)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            total -= 1
    return total


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -_count_range(end, start, holidays)
    return _count_range(start, end, holidays)
