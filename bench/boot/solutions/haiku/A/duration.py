import datetime
import re

_DURATION_RE = re.compile(
    r"(-)?P"
    r"(?:([0-9]+)Y)?"
    r"(?:([0-9]+)M)?"
    r"(?:([0-9]+)W)?"
    r"(?:([0-9]+)D)?"
    r"(?:T"
    r"(?:([0-9]+)H)?"
    r"(?:([0-9]+)M)?"
    r"(?:([0-9]+)S)?"
    r")?"
)


def _is_leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def _days_in_month(y, m):
    if m == 2:
        return 29 if _is_leap(y) else 28
    if m in (4, 6, 9, 11):
        return 30
    return 31


def _days_from_civil(y, m, d):
    # Days since 1970-01-01, proleptic Gregorian, valid for any integer year.
    y -= 1 if m <= 2 else 0
    era = y // 400
    yoe = y - era * 400
    mp = m + 9 if m <= 2 else m - 3
    doy = (153 * mp + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def _civil_from_days(z):
    z += 719468
    era = z // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + 3 if mp < 10 else mp - 9
    y += 1 if m <= 2 else 0
    return y, m, d


def add_duration(dt: datetime.datetime, iso: str) -> datetime.datetime:
    if not isinstance(iso, str):
        raise ValueError("duration must be a string")
    m = _DURATION_RE.fullmatch(iso)
    if m is None:
        raise ValueError("invalid ISO 8601 duration: %r" % (iso,))

    sign_s, Y, Mo, W, D, H, Mi, S = m.groups()
    if all(g is None for g in (Y, Mo, W, D, H, Mi, S)):
        raise ValueError("duration has no components")
    if "T" in iso and H is None and Mi is None and S is None:
        raise ValueError("'T' must be followed by a time component")

    sign = -1 if sign_s else 1
    years = int(Y) if Y is not None else 0
    months = int(Mo) if Mo is not None else 0
    weeks = int(W) if W is not None else 0
    days = int(D) if D is not None else 0
    hours = int(H) if H is not None else 0
    minutes = int(Mi) if Mi is not None else 0
    seconds = int(S) if S is not None else 0

    # Calendar step: years and months.
    base_days = _days_from_civil(dt.year, dt.month, dt.day)
    total_months = sign * (years * 12 + months)
    if total_months != 0:
        idx = dt.year * 12 + (dt.month - 1) + total_months
        ny, nm0 = divmod(idx, 12)
        nm = nm0 + 1
        nd = min(dt.day, _days_in_month(ny, nm))
        base_days = _days_from_civil(ny, nm, nd)

    # Exact elapsed time: weeks, days, hours, minutes, seconds.
    elapsed = sign * (weeks * 604800 + days * 86400 + hours * 3600
                      + minutes * 60 + seconds)
    day_seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
    total = base_days * 86400 + day_seconds + elapsed

    new_days, rem = divmod(total, 86400)
    y, mo, d = _civil_from_days(new_days)
    if not (1 <= y <= 9999):
        raise ValueError("result outside years 1 to 9999")

    hh, rem = divmod(rem, 3600)
    mm, ss = divmod(rem, 60)

    return dt.replace(year=y, month=mo, day=d,
                      hour=hh, minute=mm, second=ss)
