def parse_csv(text: str) -> list[list[str]]:
    n = len(text)
    if n == 0:
        return []

    records = []
    record = []
    i = 0

    while True:
        if i < n and text[i] == '"':
            # Quoted field
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
                        continue
                    i += 1
                    break
                buf.append(c)
                i += 1
            field = ''.join(buf)
            # Must be followed by ',', a record end, or end of text
            if i < n:
                c = text[i]
                if c == ',' or c == '\n':
                    pass
                elif c == '\r' and i + 1 < n and text[i + 1] == '\n':
                    pass
                else:
                    raise ValueError("unexpected character after quoted field")
        else:
            # Unquoted field: a double quote here is ordinary data
            start = i
            while i < n:
                c = text[i]
                if c == ',' or c == '\n':
                    break
                if c == '\r' and i + 1 < n and text[i + 1] == '\n':
                    break
                i += 1
            field = text[start:i]

        record.append(field)

        if i >= n:
            records.append(record)
            break

        c = text[i]
        if c == ',':
            i += 1
            continue

        # Record end
        if c == '\n':
            i += 1
        else:  # "\r\n"
            i += 2
        records.append(record)
        record = []
        if i >= n:
            break

    return records
