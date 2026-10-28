def canonical_json(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return _escape_string(v)
    if isinstance(v, list):
        return "[" + ",".join(canonical_json(item) for item in v) + "]"
    if isinstance(v, dict):
        # Sort keys by comparing them as sequences of UTF-16 code units.
        # In Python, string comparison is lexicographical based on Unicode code points,
        # which matches the UTF-16 sequence comparison for the BMP.
        sorted_keys = sorted(v.keys())
        items = []
        for k in sorted_keys:
            items.append(f"{_escape_string(k)}:{canonical_json(v[k])}")
        return "{" + ",".join(items) + "}"
    raise ValueError("Unsupported type")

def _escape_string(s: str) -> str:
    res = []
    for char in s:
        cp = ord(char)
        if char == '"':
            res.append('\\"')
        elif char == '\\':
            res.append('\\\\')
        elif char == '\b':
            res.append('\\b')
        elif char == '\f':
            res.append('\\f')
        elif char == '\n':
            res.append('\\n')
        elif char == '\r':
            res.append('\\r')
        elif char == '\t':
            res.append('\\t')
        elif cp < 0x20:
            res.append(f"\\u{cp:04x}")
        else:
            res.append(char)
    return '"' + "".join(res) + '"'
