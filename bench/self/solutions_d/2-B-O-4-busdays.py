import datetime


def _weekdays_before(n: int) -> int:
    # Count weekdays among ordinals 1..n-1 relative to a fixed anchor,
    # using ordinal 1 == 0001-01-01, which is a Monday.
    # Weekday index of ordinal k is (k - 1) % 7, where 0..4 are Mon..Fri.
    # Count weekdays among ordinals in [1, n).
    if n <= 1:
        return 0
    m = n - 1  # ordinals 1..m
    full_weeks, rem = divmod(m, 7)
    count = full_weeks * 5
    # remaining ordinals are 7*full_weeks + 1 .. m; their indices are 0..rem-1
    count += min(rem, 5)
    return count


def _count_range(start: datetime.date, end: datetime.date,
                 holidays: set[datetime.date]) -> int:
    # Count weekdays d with start <= d < end, minus holidays on weekdays.
    s = start.toordinal()
    e = end.toordinal()
    if e <= s:
        return 0
    total = _weekdays_before(e) - _weekdays_before(s)
    for h in holidays:
        ho = h.toordinal()
        if s <= ho < e and h.weekday() < 5:
            total -= 1
    return total


def business_days(start: datetime.date, end: datetime.date,
                  holidays: set[datetime.date]) -> int:
    if end < start:
        return -_count_range(end, start, holidays)
    return _count_range(start, end, holidays)
