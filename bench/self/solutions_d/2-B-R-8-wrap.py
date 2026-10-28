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
    for pi, lines in enumerate(paragraphs):
        if pi > 0:
            out.append("")
        words = " ".join(lines).split()
        line = ""
        for word in words:
            if len(word) > width:
                if line:
                    out.append(line)
                    line = ""
                for i in range(0, len(word), width):
                    out.append(word[i:i + width])
                continue
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= width:
                line = line + " " + word
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
    return out
