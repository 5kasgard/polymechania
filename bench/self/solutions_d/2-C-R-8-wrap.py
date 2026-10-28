def wrap(text: str, width: int) -> list[str]:
    if not text or not text.strip():
        return []

    # Split into paragraphs at runs of blank (empty or whitespace-only) lines.
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

    out = []
    for pi, lines in enumerate(paragraphs):
        if pi > 0:
            out.append("")
        words = " ".join(lines).split()

        cur = ""
        for word in words:
            if len(word) > width:
                # Flush the current line, then cut the long word into pieces.
                if cur:
                    out.append(cur)
                    cur = ""
                for i in range(0, len(word), width):
                    out.append(word[i:i + width])
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
