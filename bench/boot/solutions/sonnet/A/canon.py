import re
import sys

_ESC_RE = re.compile(r'[\x00-\x1f"\\]')
_ESC_MAP = {
    '"': '\\"',
    '\\': '\\\\',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}
for _i in range(0x20):
    _c = chr(_i)
    if _c not in _ESC_MAP:
        _ESC_MAP[_c] = '\\u%04x' % _i


def _esc(m):
    return _ESC_MAP[m.group(0)]


def _string(s):
    return '"' + _ESC_RE.sub(_esc, s) + '"'


def _int(n):
    try:
        return str(n)
    except ValueError:
        old = sys.get_int_max_str_digits()
        sys.set_int_max_str_digits(0)
        try:
            return str(n)
        finally:
            sys.set_int_max_str_digits(old)


def _key(k):
    return k.encode('utf-16-be', 'surrogatepass')


def canonical_json(v) -> str:
    out = []
    stack = [(0, v)]
    while stack:
        kind, x = stack.pop()
        if kind == 1:
            out.append(x)
            continue
        if x is None:
            out.append('null')
        elif x is True:
            out.append('true')
        elif x is False:
            out.append('false')
        elif isinstance(x, int):
            out.append(_int(x))
        elif isinstance(x, str):
            out.append(_string(x))
        elif isinstance(x, (list, tuple)):
            if not x:
                out.append('[]')
                continue
            out.append('[')
            stack.append((1, ']'))
            for i in range(len(x) - 1, -1, -1):
                stack.append((0, x[i]))
                if i:
                    stack.append((1, ','))
        elif isinstance(x, dict):
            if not x:
                out.append('{}')
                continue
            for k in x:
                if not isinstance(k, str):
                    raise TypeError("object keys must be str")
            keys = sorted(x, key=_key)
            out.append('{')
            stack.append((1, '}'))
            for i in range(len(keys) - 1, -1, -1):
                k = keys[i]
                stack.append((0, x[k]))
                stack.append((1, _string(k) + ':'))
                if i:
                    stack.append((1, ','))
        else:
            raise TypeError("unsupported type: %s" % type(x).__name__)
    return ''.join(out)
