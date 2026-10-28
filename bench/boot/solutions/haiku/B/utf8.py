def utf8_decode(b: bytes) -> str:
    out = []
    needed = 0
    cp = 0
    lower = 0x80
    upper = 0xBF
    i = 0
    n = len(b)
    while i < n:
        byte = b[i]
        if needed == 0:
            if byte <= 0x7F:
                out.append(chr(byte))
            elif 0xC2 <= byte <= 0xDF:
                needed = 1
                cp = byte & 0x1F
            elif 0xE0 <= byte <= 0xEF:
                if byte == 0xE0:
                    lower = 0xA0
                elif byte == 0xED:
                    upper = 0x9F
                needed = 2
                cp = byte & 0x0F
            elif 0xF0 <= byte <= 0xF4:
                if byte == 0xF0:
                    lower = 0x90
                elif byte == 0xF4:
                    upper = 0x8F
                needed = 3
                cp = byte & 0x07
            else:
                out.append('\ufffd')
            i += 1
        elif not (lower <= byte <= upper):
            # Ill-formed: emit one U+FFFD for the maximal subpart so far,
            # then reprocess this byte from the initial state.
            needed = 0
            cp = 0
            lower = 0x80
            upper = 0xBF
            out.append('\ufffd')
            # do not advance i; byte is handled in the initial state
        else:
            lower = 0x80
            upper = 0xBF
            cp = (cp << 6) | (byte & 0x3F)
            needed -= 1
            i += 1
            if needed == 0:
                out.append(chr(cp))
                cp = 0
    if needed != 0:
        out.append('\ufffd')
    return ''.join(out)
