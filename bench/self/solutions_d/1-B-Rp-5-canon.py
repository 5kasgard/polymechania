def canonical_json(v) -> str:
    def utf16_key(s):
        return s.encode("utf-16-be")

    def enc_str(s):
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

    parts = []
    # Stack items are either values to encode or literal strings to emit.
    stack = [("v", v)]
    while stack:
        kind, item = stack.pop()
        if kind == "lit":
            parts.append(item)
            continue
        x = item
        if x is None:
            parts.append("null")
        elif x is True:
            parts.append("true")
        elif x is False:
            parts.append("false")
        elif isinstance(x, int):
            parts.append(str(x))
        elif isinstance(x, str):
            parts.append(enc_str(x))
        elif isinstance(x, list):
            # Push in reverse so they pop in order.
            stack.append(("lit", "]"))
            for i in range(len(x) - 1, -1, -1):
                stack.append(("v", x[i]))
                if i > 0:
                    stack.append(("lit", ","))
            parts.append("[")
        elif isinstance(x, dict):
            keys = sorted(x.keys(), key=utf16_key)
            stack.append(("lit", "}"))
            for i in range(len(keys) - 1, -1, -1):
                k = keys[i]
                stack.append(("v", x[k]))
                stack.append(("lit", enc_str(k) + ":"))
                if i > 0:
                    stack.append(("lit", ","))
            parts.append("{")
        else:
            raise TypeError("unsupported type: %r" % (type(x),))
    return "".join(parts)
