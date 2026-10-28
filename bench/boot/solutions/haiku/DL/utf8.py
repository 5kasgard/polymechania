def utf8_decode(b: bytes) -> str:
    out = []
    i = 0
    n = len(b)
    while i < n:
        c = b[i]
        if c < 0x80:
            out.append(chr(c))
            i += 1
            continue
        # Determine expected length and allowed range of the second byte
        if 0xC2 <= c <= 0xDF:
            need = 1
            lo, hi = 0x80, 0xBF
        elif c == 0xE0:
            need = 2
            lo, hi = 0xA0, 0xBF
        elif 0xE1 <= c <= 0xEC or c == 0xEE or c == 0xEF:
            need = 2
            lo, hi = 0x80, 0xBF
        elif c == 0xED:
            need = 2
            lo, hi = 0x80, 0x9F
        elif c == 0xF0:
            need = 3
            lo, hi = 0x90, 0xBF
        elif 0xF1 <= c <= 0xF3:
            need = 3
            lo, hi = 0x80, 0xBF
        elif c == 0xF4:
            need = 3
            lo, hi = 0x80, 0x8F
        else:
            # Byte cannot start any sequence (0x80-0xC1, 0xF5-0xFF)
            out.append('\ufffd')
            i += 1
            continue

        # Consume the maximal valid subpart
        cp = c & (0x1F if need == 1 else 0x0F if need == 2 else 0x07)
        j = i + 1
        ok = True
        for k in range(need):
            if j >= n:
                ok = False
                break
            d = b[j]
            if k == 0:
                if d < lo or d > hi:
                    ok = False
                    break
            else:
                if d < 0x80 or d > 0xBF:
                    ok = False
                    break
            cp = (cp << 6) | (d & 0x3F)
            j += 1
        if ok:
            out.append(chr(cp))
            i = j
        else:
            # One U+FFFD for the maximal subpart; j points past consumed valid bytes
            out.append('\ufffd')
            i = j
    return ''.join(out)
