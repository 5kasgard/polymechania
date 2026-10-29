import datetime


def _weekdays_before(d: datetime.date) -> int:
    # Count weekdays in the half-open range [date(1,1,1), d).
    # Use ordinal (day 1 = Monday in proleptic Gregorian ordinal, weekday() of ordinal 1 is Monday).
    n = d.toordinal() - 1  # days strictly before d, counted from ordinal 1
    weeks, rem = divmod(n, 7)
    count = weeks * 5
    # The first `rem` days of the partial week starting at ordinal 1 (Monday) are weekdays
    # up to index 4; days 0..6 correspond to Mon..Sun.
    count += min(rem, 5)
    return count


def business_days(start: datetime.date, end: datetime.date, holidays: set) -> int:
    if end < start:
        return -business_days(end, start, holidays)
    total = _weekdays_before(end) - _weekdays_before(start)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            total -= 1
    return total
