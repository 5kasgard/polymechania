import re


def slugify(s: str) -> str:
    s = s.lower()
    # Keep only ASCII letters and digits as runs; everything else separates.
    parts = re.findall(r"[a-z0-9]+", s)
    return "-".join(parts)
