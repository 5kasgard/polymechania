def utf8_decode(b: bytes) -> str:
    out = []
    n = len(b)
    i = 0
    while i < n:
        c = b[i]
        if c < 0x80:
            out.append(chr(c))
            i += 1
            continue
        if 0xC2 <= c <= 0xDF:
            need = 1
            cp = c & 0x1F
            lo, hi = 0x80, 0xBF
        elif 0xE0 <= c <= 0xEF:
            need = 2
            cp = c & 0x0F
            lo, hi = 0x80, 0xBF
            if c == 0xE0:
                lo = 0xA0
            elif c == 0xED:
                hi = 0x9F
        elif 0xF0 <= c <= 0xF4:
            need = 3
            cp = c & 0x07
            lo, hi = 0x80, 0xBF
            if c == 0xF0:
                lo = 0x90
            elif c == 0xF4:
                hi = 0x8F
        else:
            out.append('\ufffd')
            i += 1
            continue
        i += 1
        ok = True
        while need > 0:
            if i >= n:
                ok = False
                break
            d = b[i]
            if d < lo or d > hi:
                ok = False
                break
            cp = (cp << 6) | (d & 0x3F)
            lo, hi = 0x80, 0xBF
            i += 1
            need -= 1
        if ok:
            out.append(chr(cp))
        else:
            out.append('\ufffd')
    return ''.join(out)
