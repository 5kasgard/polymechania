# NOTE: the specification for 'csv' is only the single letter "r", so the
# behaviour below is an assumed minimal reading (parse one CSV line into a
# list of fields, RFC 4180 style). Please supply the full specification.
import io


def csv(text):
    """Parse a single CSV record from text into a list of field strings.

    Supports quoted fields, doubled quotes inside quoted fields, and
    commas inside quotes. Uses the standard library only.
    """
    fields = []
    field = []
    in_quotes = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_quotes:
            if ch == '"':
                if i + 1 < n and text[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(ch)
        else:
            if ch == '"':
                in_quotes = True
            elif ch == ',':
                fields.append(''.join(field))
                field = []
            elif ch in '\r\n':
                break
            else:
                field.append(ch)
        i += 1
    fields.append(''.join(field))
    return fields
