def canonical_json(v) -> str:
    def utf16_key(s: str):
        # Sort keys by their UTF-16 code units (big-endian), per RFC 8785.
        return s.encode("utf-16-be")

    def enc_str(s: str) -> str:
        out = ['"']
        for ch in s:
            o = ord(ch)
            if ch == '"':
                out.append('\\"')
            elif ch == "\\":
                out.append("\\\\")
            elif ch == "\b":
                out.append("\\b")
            elif ch == "\f":
                out.append("\\f")
            elif ch == "\n":
                out.append("\\n")
            elif ch == "\r":
                out.append("\\r")
            elif ch == "\t":
                out.append("\\t")
            elif o < 0x20:
                out.append("\\u%04x" % o)
            else:
                out.append(ch)
        out.append('"')
        return "".join(out)

    def enc(x) -> str:
        if x is None:
            return "null"
        if x is True:
            return "true"
        if x is False:
            return "false"
        if isinstance(x, int):
            return str(int(x))
        if isinstance(x, str):
            return enc_str(x)
        if isinstance(x, list):
            return "[" + ",".join(enc(e) for e in x) + "]"
        if isinstance(x, dict):
            keys = sorted(x.keys(), key=utf16_key)
            return "{" + ",".join(enc_str(k) + ":" + enc(x[k]) for k in keys) + "}"
        raise TypeError("unsupported type: %r" % type(x))

    return enc(v)
