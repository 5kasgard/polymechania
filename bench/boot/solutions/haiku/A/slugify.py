import re

_TOKEN = re.compile(r'[a-z0-9]+')

def slugify(s: str) -> str:
    return '-'.join(_TOKEN.findall(s.lower()))
