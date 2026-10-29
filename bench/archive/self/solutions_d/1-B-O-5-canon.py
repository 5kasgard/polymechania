def canonical_json(v) -> str:
    # Escape table for the characters that need a short form.
    short = {'"': '\\"', '\\': '\\\\', '\b': '\\b', '\f': '\\f',
             '\n': '\\n', '\r': '\\r', '\t': '\\t'}

    def enc_str(s: str) -> str:
        out = ['"']
        for ch in s:
            if ch in short:
                out.append(short[ch])
            elif ord(ch) < 0x20:
                out.append('\\u%04x' % ord(ch))
            else:
                out.append(ch)
        out.append('"')
        return ''.join(out)

    def enc(x) -> str:
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
            # Sort by UTF-16 code units: encoding to UTF-16-BE gives bytes
            # whose lexicographic order equals code-unit order.
            keys = sorted(x.keys(), key=lambda k: k.encode('utf-16-be'))
            return '{' + ','.join(enc_str(k) + ':' + enc(x[k]) for k in keys) + '}'
        raise TypeError('unsupported type: %r' % type(x))

    return enc(v)
