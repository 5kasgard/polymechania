import json

def canonical_json(v) -> str:
    def escape_string(s: str) -> str:
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
                res.append(f'\\u{cp:04x}')
            else:
                res.append(char)
        return "".join(res)

    def serialize(obj) -> str:
        if obj is None:
            return "null"
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        elif isinstance(obj, int):
            return str(obj)
        elif isinstance(obj, str):
            return f'"{escape_string(obj)}"'
        elif isinstance(obj, list):
            return "[" + ",".join(serialize(item) for item in obj) + "]"
        elif isinstance(obj, dict):
            # RFC 8785: sort keys by their UTF-16 code units
            # In Python, strings are already sequences of Unicode points.
            # Comparing strings directly in Python follows Unicode code point order,
            # which is equivalent to UTF-16 code unit order for the purpose of sorting.
            sorted_keys = sorted(obj.keys())
            parts = []
            for k in sorted_keys:
                parts.append(f'"{escape_string(k)}":{serialize(obj[k])}')
            return "{" + ",".join(parts) + "}"
        else:
            raise TypeError(f"Type {type(obj)} not supported")

    return serialize(v)
