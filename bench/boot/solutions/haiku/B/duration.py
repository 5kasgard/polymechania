import calendar
import datetime
import re

_PATTERN = re.compile(
    r'(-)?P'
    r'(?:([0-9]+)Y)?'
    r'(?:([0-9]+)M)?'
    r'(?:([0-9]+)W)?'
    r'(?:([0-9]+)D)?'
    r'(?:T(?=[0-9])(?:([0-9]+)H)?(?:([0-9]+)M)?(?:([0-9]+)S)?)?'
)


def add_duration(dt: datetime.datetime, iso: str) -> datetime.datetime:
    if not isinstance(iso, str):
        raise ValueError("duration must be a string")
    m = _PATTERN.fullmatch(iso)
    if m is None:
        raise ValueError(f"invalid ISO 8601 duration: {iso!r}")
    groups = m.groups()
    if all(g is None for g in groups[1:]):
        raise ValueError("duration has no components")
    sign = -1 if groups[0] else 1
    years, months, weeks, days, hours, minutes, seconds = (
        int(g) if g is not None else 0 for g in groups[1:]
    )

    total_months = sign * (years * 12 + months)
    if total_months:
        idx = dt.year * 12 + (dt.month - 1) + total_months
        year, month0 = divmod(idx, 12)
        if not 1 <= year <= 9999:
            raise ValueError("result outside years 1 to 9999")
        month = month0 + 1
        last_day = calendar.monthrange(year, month)[1]
        day = min(dt.day, last_day)
        dt = dt.replace(year=year, month=month, day=day)

    try:
        delta = datetime.timedelta(
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
        )
        result = dt + sign * delta
    except OverflowError as exc:
        raise ValueError("result outside years 1 to 9999") from exc

    if not 1 <= result.year <= 9999:
        raise ValueError("result outside years 1 to 9999")
    return result
