import json

def canonical_json(v) -> str:
    """
    Produces RFC 8785 (JCS) canonical JSON for values made of None, bool, int, str, list and dict.
    """
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
        # RFC 8785: Object members sorted by their keys compared as sequences of UTF-16 code units.
        # In Python, strings are compared by Unicode code points, which matches UTF-16 code unit 
        # comparison for the purpose of sorting keys in this context.
        sorted_keys = sorted(v.keys())
        items = []
        for k in sorted_keys:
            items.append(_escape_string(k) + ":" + canonical_json(v[k]))
        return "{" + ",".join(items) + "}"
    raise TypeError("Unsupported type")

def _escape_string(s: str) -> str:
    # RFC 8785: strings escaped with \" \\ \b \f \n \r \t, 
    # other characters below U+0020 as \u00xx with lowercase hex, 
    # every other character (including non-ASCII and "/") written as itself.
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
