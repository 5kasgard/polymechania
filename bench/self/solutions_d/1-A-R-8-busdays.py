import datetime


def _weekdays_before(n: int) -> int:
    # Count of weekdays in the days d with 0 <= d < n, counted from a
    # reference date that is a Monday (ordinal 1 is a Monday).
    # Days ordinal o (1-based) with o mod 7 in {1,...,5} are weekdays.
    full, rem = divmod(n, 7)
    count = full * 5
    # remaining days correspond to offsets 0..rem-1 from the base Monday
    count += min(rem, 5)
    return count


def _weekdays_in_range(start: datetime.date, end: datetime.date) -> int:
    # Weekdays d with start <= d < end, assuming start <= end.
    if start >= end:
        return 0
    s = start.toordinal()
    e = end.toordinal()
    # Shift so that ordinal 1 (a Monday) maps to 0.
    return _weekdays_before(e - 1) - _weekdays_before(s - 1)


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        lo, hi = end, start
        sign = -1
    else:
        lo, hi = start, end
        sign = 1
    count = _weekdays_in_range(lo, hi)
    for h in holidays:
        if lo <= h < hi and h.weekday() < 5:
            count -= 1
    return sign * count
