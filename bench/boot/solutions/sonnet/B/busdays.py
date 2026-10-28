import datetime


def _g(m):
    return (m // 7) * 5 + min(m % 7, 5)


def business_days(start: datetime.date, end: datetime.date, holidays: set) -> int:
    a = start.toordinal()
    b = end.toordinal()
    sign = 1
    if b < a:
        a, b = b, a
        sign = -1
    if a == b:
        return 0
    total = _g(b - 1) - _g(a - 1)
    seen = set()
    for h in holidays:
        o = h.toordinal()
        if a <= o < b and (o - 1) % 7 < 5 and o not in seen:
            seen.add(o)
    total -= len(seen)
    return sign * total
