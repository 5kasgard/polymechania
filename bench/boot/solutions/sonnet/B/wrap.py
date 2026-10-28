def wrap(text: str, width: int) -> list[str]:
    norm = text.replace("\r\n", "\n").replace("\r", "\n")
    paragraphs = []
    cur_words = []
    for line in norm.split("\n"):
        ws = line.split()
        if not ws:
            if cur_words:
                paragraphs.append(cur_words)
                cur_words = []
        else:
            cur_words.extend(ws)
    if cur_words:
        paragraphs.append(cur_words)

    out = []
    for pi, words in enumerate(paragraphs):
        if pi > 0:
            out.append("")
        cur = ""
        for w in words:
            if len(w) > width:
                if cur:
                    out.append(cur)
                    cur = ""
                for i in range(0, len(w), width):
                    out.append(w[i:i + width])
                continue
            if not cur:
                cur = w
            elif len(cur) + 1 + len(w) <= width:
                cur += " " + w
            else:
                out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out
