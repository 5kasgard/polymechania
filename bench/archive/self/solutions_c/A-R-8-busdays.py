import datetime


def _weekdays_before(n: int) -> int:
    # Number of Monday-to-Friday days in the half-open range [0, n) counted
    # from a reference date that is a Monday (ordinal 0 is a Monday).
    full_weeks, rem = divmod(n, 7)
    count = full_weeks * 5
    count += min(rem, 5)
    return count


def _count_weekdays(a: datetime.date, b: datetime.date) -> int:
    # Weekdays in [a, b) where a <= b.
    if b <= a:
        return 0
    # Monday has weekday() == 0; the ordinal of a Monday satisfies
    # (ordinal - 1) % 7 == 0 with date.toordinal() where 1 is 0001-01-01 (a Monday).
    ao = a.toordinal() - 1
    bo = b.toordinal() - 1
    return _weekdays_before(bo) - _weekdays_before(ao)


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    sign = 1
    lo, hi = start, end
    if end < start:
        sign = -1
        lo, hi = end, start

    count = _count_weekdays(lo, hi)
    for h in holidays:
        if lo <= h < hi and h.weekday() < 5:
            count -= 1
    return sign * count
