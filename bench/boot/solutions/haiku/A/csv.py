def parse_csv(text: str) -> list[list[str]]:
    n = len(text)
    if n == 0:
        return []

    records = []
    rec = []
    i = 0

    while True:
        # Parse one field starting at i (i may equal n: an empty trailing field).
        if i < n and text[i] == '"':
            i += 1
            buf = []
            while True:
                if i >= n:
                    raise ValueError("unterminated quoted field")
                c = text[i]
                if c == '"':
                    if i + 1 < n and text[i + 1] == '"':
                        buf.append('"')
                        i += 2
                    else:
                        i += 1
                        break
                else:
                    buf.append(c)
                    i += 1
            field = ''.join(buf)
            if i < n and text[i] not in ',\n' and not text.startswith('\r\n', i):
                raise ValueError("characters after closing quote")
        else:
            j = i
            while j < n:
                c = text[j]
                if c == ',' or c == '\n':
                    break
                if c == '\r' and j + 1 < n and text[j + 1] == '\n':
                    break
                j += 1
            field = text[i:j]
            i = j

        rec.append(field)

        if i >= n:
            records.append(rec)
            break

        if text[i] == ',':
            i += 1
            continue

        if text[i] == '\n':
            i += 1
        else:
            # Must be "\r\n" here: the field parsers guarantee this.
            i += 2
        records.append(rec)
        rec = []
        if i >= n:
            break

    return records
