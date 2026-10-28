import datetime


def _weekdays_before(d: datetime.date) -> int:
    # Number of Monday-to-Friday days in the half-open range [epoch, d),
    # where epoch is a fixed Monday. Negative if d precedes the epoch.
    epoch = datetime.date(2000, 1, 3)  # a Monday
    delta = (d - epoch).days
    weeks, rem = divmod(delta, 7)  # rem in 0..6, days past the last whole week
    count = weeks * 5
    # rem days after a Monday: contribute min(rem, 5) weekdays
    count += min(rem, 5)
    return count


def business_days(start: datetime.date, end: datetime.date,
                  holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)
    total = _weekdays_before(end) - _weekdays_before(start)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            total -= 1
    return total
