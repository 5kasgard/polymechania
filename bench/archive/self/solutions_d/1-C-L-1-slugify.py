import re


def slugify(s: str) -> str:
    s = s.lower()
    parts = re.findall(r"[a-z0-9]+", s)
    return "-".join(parts)
