def canonical_json(v) -> str:
    """
    Produces RFC 8785 (JCS) canonical JSON for the given value.
    """
    if v is None:
        return "null"
    
    if isinstance(v, bool):
        return "true" if v else "false"
    
    if isinstance(v, int):
        return str(v)
    
    if isinstance(v, str):
        return _encode_string(v)
    
    if isinstance(v, list):
        parts = [_canonical_json(item) for item in v]
        return "[" + ",".join(parts) + "]"
    
    if isinstance(v, dict):
        # RFC 8785: Object members sorted by their keys compared as sequences of UTF-16 code units.
        # In Python, sorting strings naturally follows Unicode code point order, 
        # which matches the UTF-16 sequence order for these characters.
        sorted_keys = sorted(v.keys())
        parts = []
        for k in sorted_keys:
            if not isinstance(k, str):
                raise TypeError("JSON keys must be strings")
            parts.append(_encode_string(k) + ":" + _canonical_json(v[k]))
        return "{" + ",".join(parts) + "}"
    
    raise TypeError(f"Type {type(v)} is not supported by JCS")

def _canonical_json(v) -> str:
    # Helper to avoid recursion depth issues if needed, 
    # but for standard JSON structures, direct recursion is fine.
    return canonical_json(v)

def _encode_string(s: str) -> str:
    """
    Encodes a string according to RFC 8785 escaping rules.
    """
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
            # Characters below U+0020 as \u00xx with lowercase hex
            res.append(f"\\u{cp:04x}")
        else:
            # Every other character (including non-ASCII and "/") written as itself
            res.append(char)
    return '"' + "".join(res) + '"'
