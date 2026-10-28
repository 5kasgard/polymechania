import datetime
import calendar
import re

_PAT = re.compile(
    r"(-)?P(?:([0-9]+)Y)?(?:([0-9]+)M)?(?:([0-9]+)W)?(?:([0-9]+)D)?"
    r"(?:(T)(?:([0-9]+)H)?(?:([0-9]+)M)?(?:([0-9]+)S)?)?"
)


def add_duration(dt: datetime.datetime, iso: str) -> datetime.datetime:
    if not isinstance(iso, str):
        raise ValueError("invalid duration")
    m = _PAT.fullmatch(iso)
    if m is None:
        raise ValueError("invalid duration")
    neg, y, mo, w, d, t, h, mi, s = m.groups()
    if t is not None and h is None and mi is None and s is None:
        raise ValueError("invalid duration")
    if all(x is None for x in (y, mo, w, d, h, mi, s)):
        raise ValueError("invalid duration")
    sign = -1 if neg else 1
    y = int(y) if y else 0
    mo = int(mo) if mo else 0
    w = int(w) if w else 0
    d = int(d) if d else 0
    h = int(h) if h else 0
    mi = int(mi) if mi else 0
    s = int(s) if s else 0

    total = dt.year * 12 + (dt.month - 1) + sign * (y * 12 + mo)
    ny, nm = divmod(total, 12)
    nm += 1
    if ny < 1 or ny > 9999:
        raise ValueError("result out of range")
    nd = min(dt.day, calendar.monthrange(ny, nm)[1])
    try:
        cur = dt.replace(year=ny, month=nm, day=nd)
        delta = datetime.timedelta(weeks=w, days=d, hours=h, minutes=mi, seconds=s)
        if sign < 0:
            delta = -delta
        return cur + delta
    except OverflowError:
        raise ValueError("result out of range")
