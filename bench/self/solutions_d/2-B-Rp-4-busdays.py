import datetime


def _weekdays_before(ordinal: int) -> int:
    # Number of weekdays (Mon-Fri) among ordinals 1 .. ordinal-1 (exclusive of ordinal).
    # Ordinal 1 is 0001-01-01, a Monday, so ordinal % 7 gives weekday with Monday=1 ... Sunday=0.
    full_weeks, rem = divmod(ordinal - 1, 7)
    # rem days of the partial week starting on Monday: count how many are Mon-Fri.
    partial = min(rem, 5)
    return full_weeks * 5 + partial


def _count_forward(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    s = start.toordinal()
    e = end.toordinal()
    total = _weekdays_before(e) - _weekdays_before(s)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            total -= 1
    return total


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end >= start:
        return _count_forward(start, end, holidays)
    return -_count_forward(end, start, holidays)
