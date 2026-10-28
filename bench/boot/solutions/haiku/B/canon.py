# NOTE: ints are rendered with str(); Python 3.11+ may refuse integers with more than 4300 digits.
def _quote(s):
    parts = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            parts.append('\\"')
        elif ch == '\\':
            parts.append('\\\\')
        elif o == 0x08:
            parts.append('\\b')
        elif o == 0x0C:
            parts.append('\\f')
        elif o == 0x0A:
            parts.append('\\n')
        elif o == 0x0D:
            parts.append('\\r')
        elif o == 0x09:
            parts.append('\\t')
        elif o < 0x20:
            parts.append('\\u%04x' % o)
        else:
            parts.append(ch)
    parts.append('"')
    return ''.join(parts)


def _utf16_key(s):
    return s.encode('utf-16-be', 'surrogatepass')


def canonical_json(v):
    out = []
    # Explicit stack of tokens: ('v', value) for values, ('raw', text) for literal text.
    stack = [('v', v)]
    while stack:
        kind, item = stack.pop()
        if kind == 'raw':
            out.append(item)
            continue
        if item is None:
            out.append('null')
        elif isinstance(item, bool):
            out.append('true' if item else 'false')
        elif isinstance(item, int):
            out.append(str(item))
        elif isinstance(item, str):
            out.append(_quote(item))
        elif isinstance(item, list):
            seq = [('raw', '[')]
            for i, x in enumerate(item):
                if i > 0:
                    seq.append(('raw', ','))
                seq.append(('v', x))
            seq.append(('raw', ']'))
            stack.extend(reversed(seq))
        elif isinstance(item, dict):
            for k in item:
                if not isinstance(k, str):
                    raise TypeError('object keys must be str')
            keys = sorted(item, key=_utf16_key)
            seq = [('raw', '{')]
            for i, k in enumerate(keys):
                if i > 0:
                    seq.append(('raw', ','))
                seq.append(('raw', _quote(k) + ':'))
                seq.append(('v', item[k]))
            seq.append(('raw', '}'))
            stack.extend(reversed(seq))
        else:
            raise TypeError('unsupported type: %s' % type(item).__name__)
    return ''.join(out)
