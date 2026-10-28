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
            lo, hi = 0x80, 0xBF
            cp = c & 0x1F
        elif 0xE0 <= c <= 0xEF:
            need = 2
            lo, hi = 0x80, 0xBF
            if c == 0xE0:
                lo = 0xA0
            elif c == 0xED:
                hi = 0x9F
            cp = c & 0x0F
        elif 0xF0 <= c <= 0xF4:
            need = 3
            lo, hi = 0x80, 0xBF
            if c == 0xF0:
                lo = 0x90
            elif c == 0xF4:
                hi = 0x8F
            cp = c & 0x07
        else:
            out.append('\ufffd')
            i += 1
            continue
        j = i + 1
        ok = True
        for _ in range(need):
            if j < n and lo <= b[j] <= hi:
                cp = (cp << 6) | (b[j] & 0x3F)
                j += 1
                lo, hi = 0x80, 0xBF
            else:
                ok = False
                break
        if ok:
            out.append(chr(cp))
        else:
            out.append('\ufffd')
        i = j
    return ''.join(out)
