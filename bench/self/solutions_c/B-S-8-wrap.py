def wrap(text: str, width: int) -> list[str]:
    # Split into lines, then group into paragraphs separated by blank lines.
    lines = text.splitlines()
    paragraphs = []
    current = []
    for line in lines:
        if line.strip() == "":
            if current:
                paragraphs.append(current)
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append(current)

    out = []
    for pi, para in enumerate(paragraphs):
        if pi > 0:
            out.append("")
        words = []
        for line in para:
            words.extend(line.split())

        cur = ""  # current line being built ("" means no line in progress)
        for word in words:
            if len(word) > width:
                # Flush any partial line, then cut the long word into pieces.
                if cur:
                    out.append(cur)
                    cur = ""
                for start in range(0, len(word), width):
                    out.append(word[start:start + width])
                # Following word must start a new line; the last piece has
                # already been emitted as its own line.
                cur = ""
                continue
            if not cur:
                cur = word
            elif len(cur) + 1 + len(word) <= width:
                cur = cur + " " + word
            else:
                out.append(cur)
                cur = word
        if cur:
            out.append(cur)

    return out
