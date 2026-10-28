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

    def sort_key(key: str):
        # RFC 8785: keys sorted as sequences of UTF-16 code units
        # Python strings are Unicode; we convert to UTF-16 code units
        return list(key.encode('utf-16-le'))

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
            parts = [serialize(item) for item in obj]
            return "[" + ",".join(parts) + "]"
        elif isinstance(obj, dict):
            # Sort keys by UTF-16 code units
            sorted_keys = sorted(obj.keys(), key=sort_key)
            parts = []
            for k in sorted_keys:
                parts.append(f'"{escape_string(k)}":{serialize(obj[k])}')
            return "{" + ",".join(parts) + "}"
        else:
            raise TypeError(f"Type {type(obj)} not supported")

    return serialize(v)
