import datetime


def _weekdays_before(n: int) -> int:
    # Number of weekday ordinals in [1, n). Ordinal 1 is a Monday.
    q, r = divmod(n - 1, 7)
    return 5 * q + min(r, 5)


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)

    a = start.toordinal()
    b = end.toordinal()
    count = _weekdays_before(b) - _weekdays_before(a)

    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            count -= 1
    return count
