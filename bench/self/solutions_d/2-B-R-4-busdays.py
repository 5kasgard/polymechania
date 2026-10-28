import datetime


def _weekdays_before(n: int) -> int:
    # Count of Monday-to-Friday days in the first n days counted from a
    # reference Monday (day 0 is a Monday, days 0..4 of each week are weekdays).
    if n <= 0:
        return 0
    weeks, rem = divmod(n, 7)
    return weeks * 5 + min(rem, 5)


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)

    # Ordinal day numbers: date.toordinal() gives 1 for 0001-01-01 (a Monday).
    # Weekday of ordinal o: (o - 1) % 7 gives 0 for Monday.
    s = start.toordinal()
    e = end.toordinal()

    def weekdays_in_ordinal_range(lo: int, hi: int) -> int:
        # Weekdays among ordinals in [lo, hi).
        # Shift so that ordinal 1 (Monday) maps to 0.
        return _weekdays_before(hi - 1) - _weekdays_before(lo - 1)

    total = weekdays_in_ordinal_range(s, e)

    for h in holidays:
        o = h.toordinal()
        if s <= o < e and h.weekday() < 5:
            total -= 1

    return total
