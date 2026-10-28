def parse_csv(text: str) -> list[list[str]]:
    n = len(text)
    records = []
    i = 0
    while i < n:
        rec = []
        while True:
            if i < n and text[i] == '"':
                parts = []
                pos = i + 1
                while True:
                    q = text.find('"', pos)
                    if q < 0:
                        raise ValueError("unterminated quoted field")
                    if q + 1 < n and text[q + 1] == '"':
                        parts.append(text[pos:q + 1])
                        pos = q + 2
                    else:
                        parts.append(text[pos:q])
                        j = q + 1
                        break
                rec.append("".join(parts))
                if j >= n:
                    i = n
                    break
                c = text[j]
                if c == ',':
                    i = j + 1
                    continue
                if c == '\n':
                    i = j + 1
                    break
                if c == '\r' and j + 1 < n and text[j + 1] == '\n':
                    i = j + 2
                    break
                raise ValueError("garbage after closing quote")
            else:
                j = i
                while j < n and text[j] != ',' and text[j] != '\n':
                    j += 1
                if j >= n:
                    rec.append(text[i:n])
                    i = n
                    break
                if text[j] == ',':
                    rec.append(text[i:j])
                    i = j + 1
                    continue
                # newline
                end = j
                if end > i and text[end - 1] == '\r':
                    end -= 1
                rec.append(text[i:end])
                i = j + 1
                break
        records.append(rec)
    return records
