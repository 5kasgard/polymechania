import datetime


def _weekdays_before(d: datetime.date) -> int:
    # Number of weekdays (Mon-Fri) in the ordinal range [1, d.toordinal()).
    # Use a fixed reference: ordinal 1 is 0001-01-01, a Monday.
    n = d.toordinal() - 1  # days in [1, d)
    weeks, rem = divmod(n, 7)
    # rem days after the last full week start on Monday, so the first rem
    # days of a week are Mon..Sun; weekdays among them are min(rem, 5).
    return weeks * 5 + min(rem, 5)


def _count_range(start: datetime.date, end: datetime.date, holidays: set) -> int:
    # Weekdays in [start, end) not in holidays, assuming start <= end.
    total = _weekdays_before(end) - _weekdays_before(start)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            total -= 1
    return total


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -_count_range(end, start, holidays)
    return _count_range(start, end, holidays)
