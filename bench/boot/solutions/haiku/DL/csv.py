def parse_csv(text: str) -> list[list[str]]:
    records: list[list[str]] = []
    n = len(text)
    i = 0
    if n == 0:
        return records
    while True:
        # parse one record starting at i
        fields: list[str] = []
        while True:
            if i < n and text[i] == '"':
                # quoted field
                i += 1
                buf: list[str] = []
                closed = False
                while i < n:
                    c = text[i]
                    if c == '"':
                        if i + 1 < n and text[i + 1] == '"':
                            buf.append('"')
                            i += 2
                        else:
                            i += 1
                            closed = True
                            break
                    else:
                        buf.append(c)
                        i += 1
                if not closed:
                    raise ValueError("unterminated quoted field")
                fields.append("".join(buf))
                # must be followed by comma, record end, or end of text
                if i >= n:
                    records.append(fields)
                    return records
                if text[i] == ",":
                    i += 1
                    continue
                if text[i] == "\n":
                    i += 1
                    records.append(fields)
                    break
                if text[i] == "\r" and i + 1 < n and text[i + 1] == "\n":
                    i += 2
                    records.append(fields)
                    break
                raise ValueError("unexpected character after quoted field")
            else:
                # unquoted field: runs to comma or record end
                start = i
                while i < n and text[i] not in (",", "\n") and not (
                    text[i] == "\r" and i + 1 < n and text[i + 1] == "\n"
                ):
                    i += 1
                fields.append(text[start:i])
                if i >= n:
                    records.append(fields)
                    return records
                if text[i] == ",":
                    i += 1
                    continue
                if text[i] == "\n":
                    i += 1
                    records.append(fields)
                    break
                # "\r\n"
                i += 2
                records.append(fields)
                break
        if i >= n:
            return records
