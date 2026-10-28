import datetime
import re

_PATTERN = re.compile(
    r"^(-)?P"
    r"(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)W)?(?:(\d+)D)?"
    r"(?:T(?=\d)(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?$"
)


def _add_months(dt: datetime.datetime, months: int) -> datetime.datetime:
    total = dt.year * 12 + (dt.month - 1) + months
    year, month0 = divmod(total, 12)
    month = month0 + 1
    if not 1 <= year <= 9999:
        raise ValueError("result out of range")
    last_day = _days_in_month(year, month)
    day = min(dt.day, last_day)
    return dt.replace(year=year, month=month, day=day)


def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        nxt = datetime.date(year + 1, 1, 1) if year < 9999 else None
        if nxt is None:
            return 31
    else:
        nxt = datetime.date(year, month + 1, 1)
    return (nxt - datetime.timedelta(days=1)).day


def add_duration(dt: datetime.datetime, iso: str) -> datetime.datetime:
    if not isinstance(iso, str):
        raise ValueError("duration must be a string")
    m = _PATTERN.match(iso)
    if not m:
        raise ValueError(f"invalid ISO 8601 duration: {iso!r}")
    sign_neg, Y, M, W, D, H, Mi, S = m.groups()
    if all(g is None for g in (Y, M, W, D, H, Mi, S)):
        raise ValueError("duration has no components")

    sign = -1 if sign_neg else 1
    years = int(Y) if Y else 0
    months = int(M) if M else 0
    weeks = int(W) if W else 0
    days = int(D) if D else 0
    hours = int(H) if H else 0
    minutes = int(Mi) if Mi else 0
    seconds = int(S) if S else 0

    try:
        result = _add_months(dt, sign * (years * 12 + months))
        delta = datetime.timedelta(
            weeks=sign * weeks,
            days=sign * days,
            hours=sign * hours,
            minutes=sign * minutes,
            seconds=sign * seconds,
        )
        result = result + delta
    except OverflowError as exc:
        raise ValueError("result out of range") from exc

    if not 1 <= result.year <= 9999:
        raise ValueError("result out of range")
    return result
