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
        next_first = datetime.date(year + 1, 1, 1) if year < 9999 else None
        if next_first is None:
            return 31
    else:
        next_first = datetime.date(year, month + 1, 1)
    return (next_first - datetime.timedelta(days=1)).day


def add_duration(dt: datetime.datetime, iso: str) -> datetime.datetime:
    if not isinstance(iso, str):
        raise ValueError("duration must be a string")
    m = _PATTERN.match(iso)
    if not m:
        raise ValueError(f"invalid ISO 8601 duration: {iso!r}")
    sign = -1 if m.group(1) else 1
    parts = [int(g) if g is not None else 0 for g in m.groups()[1:]]
    years, months, weeks, days, hours, minutes, seconds = parts
    if not any(g is not None for g in m.groups()[1:]):
        raise ValueError("duration has no components")
    if iso.endswith("T"):
        raise ValueError("'T' must be followed by a time component")

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
