def utf8_decode(b: bytes) -> str:
    # Table per lead byte: (continuation bytes needed, lower bound, upper bound
    # for the first continuation byte, initial code point bits mask)
    out = []
    n = len(b)
    i = 0
    while i < n:
        c = b[i]
        if c <= 0x7F:
            out.append(chr(c))
            i += 1
            continue
        if 0xC2 <= c <= 0xDF:
            need, lo, hi, cp = 1, 0x80, 0xBF, c & 0x1F
        elif c == 0xE0:
            need, lo, hi, cp = 2, 0xA0, 0xBF, c & 0x0F
        elif 0xE1 <= c <= 0xEC or c == 0xEE or c == 0xEF:
            need, lo, hi, cp = 2, 0x80, 0xBF, c & 0x0F
        elif c == 0xED:
            need, lo, hi, cp = 2, 0x80, 0x9F, c & 0x0F
        elif c == 0xF0:
            need, lo, hi, cp = 3, 0x90, 0xBF, c & 0x07
        elif 0xF1 <= c <= 0xF3:
            need, lo, hi, cp = 3, 0x80, 0xBF, c & 0x07
        elif c == 0xF4:
            need, lo, hi, cp = 3, 0x80, 0x8F, c & 0x07
        else:
            # Cannot start any valid prefix (80-C1, F5-FF)
            out.append('\ufffd')
            i += 1
            continue

        j = i + 1
        ok = True
        for k in range(need):
            if j >= n:
                # Truncated: the whole maximal subpart becomes one U+FFFD
                out.append('\ufffd')
                i = n
                ok = False
                break
            d = b[j]
            if k == 0:
                valid = lo <= d <= hi
            else:
                valid = 0x80 <= d <= 0xBF
            if not valid:
                # Maximal subpart ends before this byte; do not consume it
                out.append('\ufffd')
                i = j
                ok = False
                break
            cp = (cp << 6) | (d & 0x3F)
            j += 1
        if ok:
            out.append(chr(cp))
            i = j
    return ''.join(out)
