def _utf16_key(s: str):
    # Sort key: the sequence of UTF-16 code units of s.
    return list(s.encode("utf-16-be", "surrogatepass").decode("utf-16-be").encode("utf-16-be"))


def _utf16_units(s: str) -> list[int]:
    b = s.encode("utf-16-be", "surrogatepass")
    return [int.from_bytes(b[i:i + 2], "big") for i in range(0, len(b), 2)]


_ESCAPES = {
    '"': '\\"',
    "\\": "\\\\",
    "\b": "\\b",
    "\f": "\\f",
    "\n": "\\n",
    "\r": "\\r",
    "\t": "\\t",
}


def _encode_string(s: str) -> str:
    out = ['"']
    for ch in s:
        if ch in _ESCAPES:
            out.append(_ESCAPES[ch])
        elif ord(ch) < 0x20:
            out.append("\\u%04x" % ord(ch))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def canonical_json(v) -> str:
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return str(int(v))
    if isinstance(v, str):
        return _encode_string(v)
    if isinstance(v, list):
        return "[" + ",".join(canonical_json(x) for x in v) + "]"
    if isinstance(v, dict):
        keys = sorted(v.keys(), key=_utf16_units)
        members = [_encode_string(k) + ":" + canonical_json(v[k]) for k in keys]
        return "{" + ",".join(members) + "}"
    raise TypeError("unsupported type: %r" % type(v).__name__)
