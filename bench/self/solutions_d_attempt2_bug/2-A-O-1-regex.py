# NOTE: The specification field contains only the single letter "r" and no
# actual specification text, so the required behaviour of 'regex' cannot be
# determined. This is a best-effort placeholder implementing a minimal
# regex-style matcher over the standard library `re` module.
import re


def regex(pattern, text):
    """Return all non-overlapping matches of `pattern` in `text` as a list of strings."""
    return [m.group(0) for m in re.finditer(pattern, text)]
