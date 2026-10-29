def canonical_json(v) -> str:
    # Keys are ordered by UTF-16 code units, as RFC 8785 requires.
    def utf16_key(s):
        return s.encode("utf-16-be")

    _short = {'"': '\\"', '\\': '\\\\', '\b': '\\b', '\f': '\\f',
              '\n': '\\n', '\r': '\\r', '\t': '\\t'}

    def enc_str(s):
        out = ['"']
        for ch in s:
            if ch in _short:
                out.append(_short[ch])
            elif ord(ch) < 0x20:
                out.append('\\u%04x' % ord(ch))
            else:
                out.append(ch)
        out.append('"')
        return ''.join(out)

    def enc(x):
        if x is None:
            return 'null'
        if x is True:
            return 'true'
        if x is False:
            return 'false'
        if isinstance(x, int):
            return str(int(x))
        if isinstance(x, str):
            return enc_str(x)
        if isinstance(x, list):
            return '[' + ','.join(enc(e) for e in x) + ']'
        if isinstance(x, dict):
            keys = sorted(x.keys(), key=utf16_key)
            return '{' + ','.join(enc_str(k) + ':' + enc(x[k]) for k in keys) + '}'
        raise TypeError('unsupported type: %r' % type(x))

    return enc(v)
