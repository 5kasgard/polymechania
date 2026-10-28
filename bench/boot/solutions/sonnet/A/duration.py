import re
import calendar
import datetime

_RE = re.compile(
    r"(-)?P(?:([0-9]+)Y)?(?:([0-9]+)M)?(?:([0-9]+)W)?(?:([0-9]+)D)?"
    r"(?:(T)(?:([0-9]+)H)?(?:([0-9]+)M)?(?:([0-9]+)S)?)?"
)


def add_duration(dt: datetime.datetime, iso: str) -> datetime.datetime:
    if not isinstance(iso, str):
        raise ValueError("invalid duration")
    m = _RE.fullmatch(iso)
    if m is None:
        raise ValueError("invalid duration")
    neg, y, mo, w, d, t, h, mi, s = m.groups()
    if t is not None and h is None and mi is None and s is None:
        raise ValueError("invalid duration")
    if all(x is None for x in (y, mo, w, d, h, mi, s)):
        raise ValueError("invalid duration")
    sign = -1 if neg else 1
    Y = int(y) if y else 0
    M = int(mo) if mo else 0
    W = int(w) if w else 0
    D = int(d) if d else 0
    H = int(h) if h else 0
    Mi = int(mi) if mi else 0
    S = int(s) if s else 0

    result = dt
    if Y or M:
        total = dt.year * 12 + (dt.month - 1) + sign * (12 * Y + M)
        ny, nm = divmod(total, 12)
        nm += 1
        if ny < 1 or ny > 9999:
            raise ValueError("result out of range")
        nd = min(dt.day, calendar.monthrange(ny, nm)[1])
        result = dt.replace(year=ny, month=nm, day=nd)
    try:
        delta = datetime.timedelta(
            days=sign * (7 * W + D),
            hours=sign * H,
            minutes=sign * Mi,
            seconds=sign * S,
        )
        result = result + delta
    except (OverflowError, ValueError):
        raise ValueError("result out of range")
    return result
