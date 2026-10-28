def parse_csv(text: str) -> list[list[str]]:
    n = len(text)
    records: list[list[str]] = []
    i = 0
    while i < n:
        record: list[str] = []
        while True:
            if i < n and text[i] == '"':
                # Quoted field
                i += 1
                buf: list[str] = []
                while True:
                    j = text.find('"', i)
                    if j == -1:
                        raise ValueError("unterminated quoted field")
                    buf.append(text[i:j])
                    if j + 1 < n and text[j + 1] == '"':
                        buf.append('"')
                        i = j + 2
                    else:
                        i = j + 1
                        break
                record.append(''.join(buf))
                if i == n:
                    records.append(record)
                    break
                if text[i] == ',':
                    i += 1
                    continue
                if text[i] == '\n':
                    i += 1
                    records.append(record)
                    break
                if text.startswith('\r\n', i):
                    i += 2
                    records.append(record)
                    break
                raise ValueError("invalid character after quoted field")
            else:
                # Unquoted field: '"' is ordinary here
                j = i
                while j < n:
                    c = text[j]
                    if c == ',' or c == '\n':
                        break
                    if c == '\r' and j + 1 < n and text[j + 1] == '\n':
                        break
                    j += 1
                record.append(text[i:j])
                if j == n:
                    records.append(record)
                    i = n
                    break
                if text[j] == ',':
                    i = j + 1
                    continue
                if text[j] == '\n':
                    i = j + 1
                    records.append(record)
                    break
                # "\r\n"
                i = j + 2
                records.append(record)
                break
    return records
