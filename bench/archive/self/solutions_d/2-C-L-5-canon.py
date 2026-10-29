def canonical_json(v) -> str:
    out = []
    # Stack of work items: either a value to emit, or a literal string to emit.
    stack = [("v", v)]
    while stack:
        kind, item = stack.pop()
        if kind == "s":
            out.append(item)
            continue
        val = item
        if val is None:
            out.append("null")
        elif val is True:
            out.append("true")
        elif val is False:
            out.append("false")
        elif isinstance(val, int):
            out.append(str(val))
        elif isinstance(val, str):
            out.append(_escape(val))
        elif isinstance(val, list):
            # Push in reverse so items are emitted in order.
            parts = []
            for i, x in enumerate(val):
                if i:
                    parts.append(("s", ","))
                parts.append(("v", x))
            stack.append(("s", "]"))
            stack.extend(reversed(parts))
            out.append("[")
        elif isinstance(val, dict):
            keys = sorted(val.keys(), key=lambda k: k.encode("utf-16-be"))
            parts = []
            for i, k in enumerate(keys):
                if i:
                    parts.append(("s", ","))
                parts.append(("s", _escape(k) + ":"))
                parts.append(("v", val[k]))
            stack.append(("s", "}"))
            stack.extend(reversed(parts))
            out.append("{")
        else:
            raise TypeError(f"unsupported type: {type(val).__name__}")
    return "".join(out)


def _escape(s: str) -> str:
    buf = ['"']
    for ch in s:
        if ch == '"':
            buf.append('\\"')
        elif ch == "\\":
            buf.append("\\\\")
        elif ch == "\b":
            buf.append("\\b")
        elif ch == "\f":
            buf.append("\\f")
        elif ch == "\n":
            buf.append("\\n")
        elif ch == "\r":
            buf.append("\\r")
        elif ch == "\t":
            buf.append("\\t")
        elif ord(ch) < 0x20:
            buf.append("\\u%04x" % ord(ch))
        else:
            buf.append(ch)
    buf.append('"')
    return "".join(buf)
