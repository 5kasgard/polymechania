import datetime


def _weekdays_before(n: int) -> int:
    # Number of weekday days among day indices 0..n-1, where index k is a
    # Monday when k % 7 == 0 (ordinal 1, 0001-01-01, is a Monday).
    return (n // 7) * 5 + min(n % 7, 5)


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    def count(a: datetime.date, b: datetime.date) -> int:
        # Non-holiday weekdays d with a <= d < b, assuming a <= b.
        lo = a.toordinal() - 1
        hi = b.toordinal() - 1
        total = _weekdays_before(hi) - _weekdays_before(lo)
        for h in holidays:
            if a <= h < b and h.weekday() < 5:
                total -= 1
        return total

    if start <= end:
        return count(start, end)
    return -count(end, start)
