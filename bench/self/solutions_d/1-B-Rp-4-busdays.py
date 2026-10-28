import datetime


def _weekdays_before(ordinal: int) -> int:
    # Number of weekdays in the days with ordinal in [1, ordinal),
    # where date.toordinal() gives 1 for 0001-01-01 (a Monday).
    n = ordinal - 1
    full_weeks, rem = divmod(n, 7)
    # Within the first `rem` days after a full week, weekday offsets 0..rem-1
    # (Monday = 0). Weekdays are offsets 0..4.
    return full_weeks * 5 + min(rem, 5)


def business_days(start: datetime.date, end: datetime.date,
                  holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)

    lo = start.toordinal()
    hi = end.toordinal()
    total = _weekdays_before(hi) - _weekdays_before(lo)

    # Subtract holidays that are weekdays inside [start, end).
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            total -= 1
    return total
