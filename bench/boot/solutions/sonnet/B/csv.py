import re

_UNQ = re.compile(r'[^,\n]*')


def parse_csv(text: str) -> list[list[str]]:
    n = len(text)
    records = []
    i = 0
    while i < n:
        fields = []
        while True:
            if i < n and text[i] == '"':
                i += 1
                buf = []
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
                fields.append(''.join(buf))
                if i == n:
                    break
                c = text[i]
                if c == ',':
                    i += 1
                    continue
                if c == '\n':
                    i += 1
                    break
                if c == '\r' and i + 1 < n and text[i + 1] == '\n':
                    i += 2
                    break
                raise ValueError("invalid character after closing quote")
            else:
                j = _UNQ.match(text, i).end()
                seg = text[i:j]
                if j < n and text[j] == '\n':
                    if seg.endswith('\r'):
                        seg = seg[:-1]
                    fields.append(seg)
                    i = j + 1
                    break
                elif j < n:
                    fields.append(seg)
                    i = j + 1
                    continue
                else:
                    fields.append(seg)
                    i = n
                    break
        records.append(fields)
    return records
