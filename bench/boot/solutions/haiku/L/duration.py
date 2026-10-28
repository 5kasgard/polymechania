# NOTE: none
import re
import calendar
import datetime

_DURATION_RE = re.compile(
    r"(-)?P"
    r"(?:([0-9]+)Y)?"
    r"(?:([0-9]+)M)?"
    r"(?:([0-9]+)W)?"
    r"(?:([0-9]+)D)?"
    r"(?:(T(?:(?:[0-9]+H)?(?:[0-9]+M)?(?:[0-9]+S)?)))?"
)


def _parse_components(iso):
    if not isinstance(iso, str):
        raise ValueError("duration must be a string")
    m = re.fullmatch(
        r"(-)?P"
        r"(?:([0-9]+)Y)?"
        r"(?:([0-9]+)M)?"
        r"(?:([0-9]+)W)?"
        r"(?:([0-9]+)D)?"
        r"(?:T((?:[0-9]+H)?(?:[0-9]+M)?(?:[0-9]+S)?))?",
        iso,
    )
    if m is None:
        raise ValueError("invalid ISO 8601 duration: %r" % (iso,))
    sign_s, y, mo, w, d, time_part = m.groups()
    if time_part is not None and time_part == "":
        raise ValueError("'T' must be followed by a time component")
    if all(g is None for g in (y, mo, w, d, time_part)):
        raise ValueError("duration has no components")
    sign = -1 if sign_s else 1

    hours = minutes = seconds = 0
    if time_part:
        tm = re.fullmatch(
            r"(?:([0-9]+)H)?(?:([0-9]+)M)?(?:([0-9]+)S)?", time_part
        )
        h, mi, s = tm.groups()
        hours = int(h) if h else 0
        minutes = int(mi) if mi else 0
        seconds = int(s) if s else 0

    years = int(y) if y else 0
    months = int(mo) if mo else 0
    weeks = int(w) if w else 0
    days = int(d) if d else 0
    return sign, years, months, weeks, days, hours, minutes, seconds


def add_duration(dt: datetime.datetime, iso: str) -> datetime.datetime:
    sign, years, months, weeks, days, hours, minutes, seconds = _parse_components(iso)
    try:
        total_months = sign * (years * 12 + months)
        if total_months:
            idx = dt.year * 12 + (dt.month - 1) + total_months
            new_year, new_month_index = divmod(idx, 12)
            new_month = new_month_index + 1
            if new_year < 1 or new_year > 9999:
                raise ValueError("result outside years 1 to 9999")
            last_day = calendar.monthrange(new_year, new_month)[1]
            new_day = min(dt.day, last_day)
            dt = dt.replace(year=new_year, month=new_month, day=new_day)

        delta = datetime.timedelta(
            weeks=sign * weeks,
            days=sign * days,
            hours=sign * hours,
            minutes=sign * minutes,
            seconds=sign * seconds,
        )
        result = dt + delta
    except OverflowError:
        raise ValueError("result outside years 1 to 9999")
    if result.year < 1 or result.year > 9999:
        raise ValueError("result outside years 1 to 9999")
    return result
