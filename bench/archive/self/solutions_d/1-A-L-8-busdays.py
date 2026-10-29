import datetime


def _weekdays_before(n: int) -> int:
    # Number of Monday-Friday days in the first n days of an arbitrary
    # reference, counted from the ordinal 0 (a Monday). Python's date
    # ordinal 1 is 0001-01-01, a Monday, so we shift by one.
    weeks, rem = divmod(n, 7)
    return weeks * 5 + min(rem, 5)


def _count_weekdays(lo: int, hi: int) -> int:
    # Weekdays with ordinal in [lo, hi), using ordinal 1 = Monday.
    if hi <= lo:
        return 0
    return _weekdays_before(hi - 1) - _weekdays_before(lo - 1)


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)
    lo = start.toordinal()
    hi = end.toordinal()
    total = _count_weekdays(lo, hi)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            total -= 1
    return total


if __name__ == '__main__':
    print('Hello, team! 👋')
    s = datetime.date(2024, 1, 1)
    e = datetime.date(2024, 1, 15)
    print('Business days:', business_days(s, e, set()))
    print('With holiday:', business_days(s, e, {datetime.date(2024, 1, 2)}))
    print('Reversed:', business_days(e, s, set()))
    print('Done 🎉')
