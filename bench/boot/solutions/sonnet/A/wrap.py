def wrap(text: str, width: int) -> list[str]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    paragraphs = []
    cur = []
    for ln in lines:
        if ln.strip() == "":
            if cur:
                paragraphs.append(cur)
                cur = []
        else:
            cur.extend(ln.split())
    if cur:
        paragraphs.append(cur)

    out = []
    for pi, words in enumerate(paragraphs):
        if pi > 0:
            out.append("")
        line = ""
        has = False
        for w in words:
            if len(w) > width:
                if has:
                    out.append(line)
                    line = ""
                    has = False
                for i in range(0, len(w), width):
                    out.append(w[i:i + width])
            elif not has:
                line = w
                has = True
            elif len(line) + 1 + len(w) <= width:
                line += " " + w
            else:
                out.append(line)
                line = w
                has = True
        if has:
            out.append(line)
    return out
