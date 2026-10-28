import re


def slugify(s: str) -> str:
    s = s.lower()
    # Keep only ASCII letters and digits as token characters; every maximal
    # run of anything else collapses to a single "-".
    parts = re.findall(r"[a-z0-9]+", s)
    return "-".join(parts)
