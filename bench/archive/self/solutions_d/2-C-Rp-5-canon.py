def _escape_string(s: str) -> str:
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == '\\':
            out.append('\\\\')
        elif ch == '\b':
            out.append('\\b')
        elif ch == '\f':
            out.append('\\f')
        elif ch == '\n':
            out.append('\\n')
        elif ch == '\r':
            out.append('\\r')
        elif ch == '\t':
            out.append('\\t')
        elif o < 0x20:
            out.append('\\u%04x' % o)
        else:
            out.append(ch)
    out.append('"')
    return ''.join(out)


def _utf16_key(s: str) -> bytes:
    # UTF-16-BE byte strings compare the same way as UTF-16 code unit sequences.
    return s.encode('utf-16-be', 'surrogatepass')


def _encode(v) -> str:
    if v is None:
        return 'null'
    if v is True:
        return 'true'
    if v is False:
        return 'false'
    if isinstance(v, int):
        return str(int(v))
    if isinstance(v, str):
        return _escape_string(v)
    if isinstance(v, list):
        return '[' + ','.join(_encode(x) for x in v) + ']'
    if isinstance(v, dict):
        keys = sorted(v.keys(), key=_utf16_key)
        return '{' + ','.join(_escape_string(k) + ':' + _encode(v[k]) for k in keys) + '}'
    raise TypeError('unsupported type: %r' % type(v).__name__)


def canonical_json(v) -> str:
    return _encode(v)
