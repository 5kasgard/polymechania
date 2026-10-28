import sys

_TABLE = {i: "\\u%04x" % i for i in range(0x20)}
_TABLE.update({
    0x22: '\\"',
    0x5C: '\\\\',
    0x08: '\\b',
    0x0C: '\\f',
    0x0A: '\\n',
    0x0D: '\\r',
    0x09: '\\t',
})

try:
    sys.set_int_max_str_digits(0)
except AttributeError:
    pass


def _quote(s):
    return '"' + s.translate(_TABLE) + '"'


def canonical_json(v) -> str:
    out = []
    stack = [(0, v)]  # (0, value) to process, (1, text) raw text
    while stack:
        kind, item = stack.pop()
        if kind == 1:
            out.append(item)
            continue
        x = item
        if x is None:
            out.append("null")
        elif x is True:
            out.append("true")
        elif x is False:
            out.append("false")
        elif isinstance(x, int):
            out.append(str(int(x)))
        elif isinstance(x, str):
            out.append(_quote(x))
        elif isinstance(x, (list, tuple)):
            if not x:
                out.append("[]")
                continue
            seq = [(1, "[")]
            first = True
            for e in x:
                if not first:
                    seq.append((1, ","))
                first = False
                seq.append((0, e))
            seq.append((1, "]"))
            stack.extend(reversed(seq))
        elif isinstance(x, dict):
            if not x:
                out.append("{}")
                continue
            for k in x:
                if not isinstance(k, str):
                    raise TypeError("keys must be str")
            items = sorted(x.items(),
                           key=lambda kv: kv[0].encode('utf-16-be', 'surrogatepass'))
            seq = [(1, "{")]
            first = True
            for k, e in items:
                if not first:
                    seq.append((1, ","))
                first = False
                seq.append((1, _quote(k) + ":"))
                seq.append((0, e))
            seq.append((1, "}"))
            stack.extend(reversed(seq))
        else:
            raise TypeError("unsupported type: %s" % type(x).__name__)
    return "".join(out)
