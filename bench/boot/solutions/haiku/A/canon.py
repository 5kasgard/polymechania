def _utf16_key(s):
    # Byte order of UTF-16BE equals code-unit order; surrogatepass keeps lone surrogates encodable.
    return s.encode('utf-16-be', 'surrogatepass')


_SHORT_ESCAPES = {
    '"': '\\"',
    '\\': '\\\\',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}


def _escape_string(s):
    parts = ['"']
    for ch in s:
        esc = _SHORT_ESCAPES.get(ch)
        if esc is not None:
            parts.append(esc)
        elif ch < '\u0020':
            parts.append('\\u%04x' % ord(ch))
        else:
            parts.append(ch)
    parts.append('"')
    return ''.join(parts)


def canonical_json(v) -> str:
    out = []
    # Explicit stack of (kind, payload): 'lit' emits text, 'val' encodes a value.
    stack = [('val', v)]
    while stack:
        kind, x = stack.pop()
        if kind == 'lit':
            out.append(x)
            continue
        if x is None:
            out.append('null')
        elif x is True:
            out.append('true')
        elif x is False:
            out.append('false')
        elif isinstance(x, int):
            out.append(str(x))
        elif isinstance(x, str):
            out.append(_escape_string(x))
        elif isinstance(x, list):
            seq = [('lit', '[')]
            for i, item in enumerate(x):
                if i:
                    seq.append(('lit', ','))
                seq.append(('val', item))
            seq.append(('lit', ']'))
            stack.extend(reversed(seq))
        elif isinstance(x, dict):
            seq = [('lit', '{')]
            for i, k in enumerate(sorted(x, key=_utf16_key)):
                if i:
                    seq.append(('lit', ','))
                seq.append(('lit', _escape_string(k)))
                seq.append(('lit', ':'))
                seq.append(('val', x[k]))
            seq.append(('lit', '}'))
            stack.extend(reversed(seq))
        else:
            raise TypeError('unsupported type for canonical_json: %r' % type(x).__name__)
    return ''.join(out)
