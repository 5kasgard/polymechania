def slugify(s: str) -> str:
    s = s.lower()
    out = []
    pending = False
    for c in s:
        if ('a' <= c <= 'z') or ('0' <= c <= '9'):
            if pending and out:
                out.append('-')
            pending = False
            out.append(c)
        else:
            pending = True
    return ''.join(out)
