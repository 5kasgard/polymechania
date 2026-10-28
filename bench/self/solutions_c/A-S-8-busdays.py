import datetime


def _weekdays_before(ordinal: int) -> int:
    # Weekdays among ordinals 1 .. ordinal-1; ordinal 1 (0001-01-01) is a Monday.
    k = ordinal - 1
    return 5 * (k // 7) + min(k % 7, 5)


def _count(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    s = start.toordinal()
    e = end.toordinal()
    total = _weekdays_before(e) - _weekdays_before(s)
    for h in holidays:
        if s <= h.toordinal() < e and h.weekday() < 5:
            total -= 1
    return total


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -_count(end, start, holidays)
    return _count(start, end, holidays)
