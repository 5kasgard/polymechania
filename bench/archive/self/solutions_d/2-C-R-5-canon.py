def canonical_json(v) -> str:
    def enc_str(s: str) -> str:
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
        if isinstance(x, (list, tuple)):
            return '[' + ','.join(enc(e) for e in x) + ']'
        if isinstance(x, dict):
            def utf16_key(k):
                b = k.encode('utf-16-be', 'surrogatepass')
                return [int.from_bytes(b[i:i + 2], 'big') for i in range(0, len(b), 2)]
            items = sorted(x.items(), key=lambda kv: utf16_key(kv[0]))
            return '{' + ','.join(enc_str(k) + ':' + enc(val) for k, val in items) + '}'
        raise TypeError('unsupported type: %r' % type(x))

    return enc(v)
