import datetime


def _weekdays_before(d: datetime.date, ref: datetime.date) -> int:
    # Count weekdays in [ref, d) for ref <= d, using arithmetic on whole weeks.
    total_days = (d - ref).days
    if total_days <= 0:
        return 0
    full_weeks, rem = divmod(total_days, 7)
    count = full_weeks * 5
    # Count weekdays among the remaining `rem` days starting at ref + full_weeks*7.
    base_wd = (ref + datetime.timedelta(days=full_weeks * 7)).weekday()
    for i in range(rem):
        if (base_wd + i) % 7 < 5:
            count += 1
    return count


def business_days(start: datetime.date, end: datetime.date,
                  holidays: set[datetime.date]) -> int:
    if end < start:
        return -business_days(end, start, holidays)
    if end == start:
        return 0
    result = _weekdays_before(end, start)
    for h in holidays:
        if start <= h < end and h.weekday() < 5:
            result -= 1
    return result


if __name__ == '__main__':
    print("Hello from the busdays desk! 🌟")
    d0 = datetime.date(2024, 1, 1)   # Monday
    d1 = datetime.date(2024, 1, 8)   # next Monday
    print("Week of Jan 1-7 2024:", business_days(d0, d1, set()))           # 5
    print("With Jan 2 holiday:  ", business_days(d0, d1, {datetime.date(2024, 1, 2)}))  # 4
    print("Reversed range:      ", business_days(d1, d0, set()))           # -5
    big_start = datetime.date(2000, 1, 1)
    big_end = datetime.date(2100, 1, 1)
    print("Century of weekdays: ", business_days(big_start, big_end, set()), "✅")
