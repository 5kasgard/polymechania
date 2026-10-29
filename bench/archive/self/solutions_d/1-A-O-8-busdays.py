import datetime


def _weekdays_before(d: datetime.date) -> int:
    # Count weekdays in the half-open range [ordinal 1, d), where ordinal 1
    # is 0001-01-01 (a Monday). Uses whole weeks plus a remainder.
    n = d.toordinal() - 1  # number of days in [0001-01-01, d)
    weeks, rem = divmod(n, 7)
    # Each full week has 5 weekdays; the remainder covers the first `rem`
    # days of a week that starts on Monday.
    return weeks * 5 + min(rem, 5)


def business_days(start: datetime.date, end: datetime.date, holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)

    count = _weekdays_before(end) - _weekdays_before(start)

    # Remove holidays that are weekdays inside [start, end).
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            count -= 1

    return count


if __name__ == '__main__':
    print("Hello! 👋 Quick demo of business_days 📅")
    s = datetime.date(2024, 1, 1)   # Monday
    e = datetime.date(2024, 1, 8)   # next Monday
    print("Week of Jan 1-7, 2024:", business_days(s, e, set()))            # 5
    hol = {datetime.date(2024, 1, 2)}
    print("With Jan 2 holiday:", business_days(s, e, hol))                 # 4
    print("Reversed range:", business_days(e, s, set()))                   # -5
    print("Empty range:", business_days(s, s, set()))                      # 0
    print("Weekend holiday ignored:",
          business_days(s, e, {datetime.date(2024, 1, 6)}))                # 5
    print("Done ✅")
