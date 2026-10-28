import datetime


def _weekdays_before(ordinal: int) -> int:
    # Count of Mon-Fri days among ordinals 0 .. ordinal-1, where ordinal 0
    # is a fixed reference Monday (date.fromordinal(1) is a Monday).
    # Ordinal 1 (0001-01-01) is a Monday, so ordinal k has weekday (k-1) % 7
    # with Monday=0.
    full_weeks, rem = divmod(ordinal, 7)
    total = full_weeks * 5
    # Days in the partial week: positions 0..rem-1 relative to ordinal 0,
    # where ordinal 0 corresponds to a Sunday (weekday index 6 in Monday=0).
    # Offset: ordinal 0 -> Sunday. Weekday(k) = (k + 6) % 7 with Monday=0.
    for k in range(full_weeks * 7, full_weeks * 7 + rem):
        if (k + 6) % 7 < 5:
            total += 1
    return total


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
