import datetime


def _weekdays_before(n: int) -> int:
    # Number of weekdays among the days with ordinal in [1, n]
    # (ordinal 1 is 0001-01-01, a Monday).
    # Count of weekdays in days 0..n-1 relative to a Monday start.
    if n <= 0:
        return 0
    weeks, rem = divmod(n, 7)
    return weeks * 5 + min(rem, 5)


def _count_weekdays(lo: datetime.date, hi: datetime.date) -> int:
    # Weekdays d with lo <= d < hi (hi >= lo).
    # Using ordinals: ordinal 1 is Monday, so ordinal o has weekday (o-1) % 7 (0=Mon).
    a = lo.toordinal() - 1  # shift so that Monday-based index 0 aligns with a % 7 == 0
    b = hi.toordinal() - 1
    return _weekdays_before(b) - _weekdays_before(a)


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)
    count = _count_weekdays(start, end)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            count -= 1
    return count
