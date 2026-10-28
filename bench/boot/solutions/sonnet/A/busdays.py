import datetime


def _before(n):
    # weekdays among ordinals 1..n-1 (ordinal 1 is a Monday)
    m = n - 1
    return (m // 7) * 5 + min(m % 7, 5)


def business_days(start: datetime.date, end: datetime.date, holidays: set) -> int:
    sign = 1
    lo, hi = start, end
    if end < start:
        sign = -1
        lo, hi = end, start
    lo_o = lo.toordinal()
    hi_o = hi.toordinal()
    count = _before(hi_o) - _before(lo_o)
    seen = set()
    for h in holidays:
        o = h.toordinal()
        if o in seen:
            continue
        seen.add(o)
        if lo_o <= o < hi_o and (o - 1) % 7 < 5:
            count -= 1
    return sign * count
