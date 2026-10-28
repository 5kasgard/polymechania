def wrap(text: str, width: int) -> list[str]:
    paragraphs = []
    current = []
    for line in text.split("\n"):
        if line.strip() == "":
            if current:
                paragraphs.append(current)
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append(current)

    out: list[str] = []
    for pi, para_lines in enumerate(paragraphs):
        if pi > 0:
            out.append("")
        words = " ".join(para_lines).split()
        cur = ""
        for word in words:
            if len(word) > width:
                if cur:
                    out.append(cur)
                    cur = ""
                pieces = [word[i:i + width] for i in range(0, len(word), width)]
                for piece in pieces[:-1]:
                    out.append(piece)
                cur = pieces[-1]
            elif not cur:
                cur = word
            elif len(cur) + 1 + len(word) <= width:
                cur += " " + word
            else:
                out.append(cur)
                cur = word
        if cur:
            out.append(cur)
    return out
