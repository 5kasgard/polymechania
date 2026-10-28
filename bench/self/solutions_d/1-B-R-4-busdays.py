import datetime


def _weekdays_in_range(start: datetime.date, end: datetime.date) -> int:
    # Count Monday-Friday days d with start <= d < end, in O(1).
    # Anchor at a fixed Monday; days_from_anchor(d) counts days since then.
    anchor = datetime.date(2000, 1, 3)  # a Monday

    def weekday_count_before(d: datetime.date) -> int:
        # Number of weekdays in [anchor, d); may be negative if d < anchor.
        n = (d - anchor).days
        weeks, rem = divmod(n, 7)
        return weeks * 5 + min(rem, 5)

    return weekday_count_before(end) - weekday_count_before(start)


def business_days(start: datetime.date, end: datetime.date,
                  holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)

    count = _weekdays_in_range(start, end)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            count -= 1
    return count
