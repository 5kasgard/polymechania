import datetime


def _weekdays_before(n: int) -> int:
    # Count of weekdays among the days with ordinal in [1, n] relative to a
    # fixed epoch; uses a 7-day period of 5 weekdays.
    full, rem = divmod(n, 7)
    # Within a block starting on a Monday (ordinal 1 is a Monday, proleptic
    # Gregorian, datetime.date.toordinal convention), the first `rem` days of
    # the partial week contribute min(rem, 5) weekdays.
    return full * 5 + min(rem, 5)


def _count_weekdays(a: datetime.date, b: datetime.date) -> int:
    # Weekdays d with a <= d < b, for a <= b.
    return _weekdays_before(b.toordinal() - 1) - _weekdays_before(a.toordinal() - 1)


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)
    total = _count_weekdays(start, end)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            total -= 1
    return total
