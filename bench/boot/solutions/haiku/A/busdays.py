import datetime


def _weekdays_before(ordinal: int) -> int:
    # Count weekdays among ordinals 1 .. ordinal-1.
    # Ordinal 1 (0001-01-01) is a Monday, so (k-1) % 7 gives 0=Mon .. 6=Sun.
    n = ordinal - 1
    return 5 * (n // 7) + min(n % 7, 5)


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)
    if end == start:
        return 0

    count = _weekdays_before(end.toordinal()) - _weekdays_before(start.toordinal())

    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            count -= 1

    return count
