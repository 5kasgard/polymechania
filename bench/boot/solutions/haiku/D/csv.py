def parse_csv(text: str) -> list[list[str]]:
    records: list[list[str]] = []
    n = len(text)
    i = 0
    if n == 0:
        return records
    while True:
        # parse one record starting at i
        record: list[str] = []
        while True:
            # parse one field starting at i
            if i < n and text[i] == '"':
                i += 1
                buf: list[str] = []
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
                if i < n and text[i] not in ',\r\n':
                    raise ValueError("unexpected character after quoted field")
                if i < n and text[i] == '\r' and not (i + 1 < n and text[i + 1] == '\n'):
                    raise ValueError("unexpected character after quoted field")
                record.append("".join(buf))
            else:
                start = i
                while i < n and text[i] not in ',\r\n':
                    i += 1
                # a lone '\r' is ordinary data
                while i < n and text[i] == '\r' and not (i + 1 < n and text[i + 1] == '\n'):
                    i += 1
                    while i < n and text[i] not in ',\r\n':
                        i += 1
                record.append(text[start:i])
            # after a field: comma, record end, or end of text
            if i >= n:
                records.append(record)
                return records
            if text[i] == ',':
                i += 1
                continue
            if text[i] == '\r' and i + 1 < n and text[i + 1] == '\n':
                i += 2
            else:
                i += 1  # '\n'
            records.append(record)
            if i >= n:
                return records
            break
