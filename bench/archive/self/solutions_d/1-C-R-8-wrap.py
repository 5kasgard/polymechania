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
    for pi, para_lines in enumerate(paragraphs):
        if pi > 0:
            out.append("")
        words = " ".join(para_lines).split()

        line = ""
        for word in words:
            if len(word) > width:
                # Flush the current line before a long word.
                if line:
                    out.append(line)
                    line = ""
                # Cut the long word into pieces of exactly `width`.
                pieces = [word[i:i + width] for i in range(0, len(word), width)]
                for piece in pieces[:-1]:
                    out.append(piece)
                # The last piece may still be extended by nothing; the next
                # word always starts a new line, so it goes on its own line.
                out.append(pieces[-1])
                line = ""
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
