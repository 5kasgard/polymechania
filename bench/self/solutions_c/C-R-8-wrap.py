def wrap(text: str, width: int) -> list[str]:
    if not text or not text.strip():
        return []

    # Split into paragraphs at runs of blank (empty or whitespace-only) lines.
    paragraphs: list[list[str]] = []
    current: list[str] = []
    for line in text.split("\n"):
        if line.strip() == "":
            if current:
                paragraphs.append(current)
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append(current)

    output: list[str] = []
    for p_index, para_lines in enumerate(paragraphs):
        if p_index > 0:
            output.append("")

        words: list[str] = []
        for line in para_lines:
            words.extend(line.split())

        line_buf = ""
        for word in words:
            if len(word) > width:
                # Flush any pending line first.
                if line_buf:
                    output.append(line_buf)
                    line_buf = ""
                # Cut the long word into pieces of exactly `width` characters.
                pieces = [word[i:i + width] for i in range(0, len(word), width)]
                output.extend(pieces[:-1])
                # The last piece starts a fresh line; the next word may join it.
                line_buf = pieces[-1]
                continue

            if not line_buf:
                line_buf = word
            elif len(line_buf) + 1 + len(word) <= width:
                line_buf = line_buf + " " + word
            else:
                output.append(line_buf)
                line_buf = word

        if line_buf:
            output.append(line_buf)

    return output
