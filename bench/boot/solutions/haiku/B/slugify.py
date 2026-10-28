def slugify(s: str) -> str:
    out = []
    pending = False
    for ch in s.lower():
        if ('a' <= ch <= 'z') or ('0' <= ch <= '9'):
            if pending and out:
                out.append('-')
            pending = False
            out.append(ch)
        else:
            pending = True
    return ''.join(out)
