def wrap(text: str, width: int) -> list[str]:
    # Group non-blank lines into paragraphs.
    paragraphs = []
    current = []
    for line in text.splitlines():
        if line.strip():
            current.append(line)
        else:
            if current:
                paragraphs.append(current)
                current = []
    if current:
        paragraphs.append(current)

    out = []
    for p_index, lines in enumerate(paragraphs):
        if p_index > 0:
            out.append("")
        words = " ".join(lines).split()
        line = ""
        for word in words:
            if len(word) > width:
                # Flush the current line before a long word.
                if line:
                    out.append(line)
                    line = ""
                # Cut the long word into exact-width pieces.
                pieces = [word[i:i + width] for i in range(0, len(word), width)]
                out.extend(pieces[:-1])
                line = pieces[-1]
            elif not line:
                line = word
            elif len(line) + 1 + len(word) <= width:
                line += " " + word
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
    return out


if __name__ == '__main__':
    sample = "The quick brown fox jumps over the lazy dog.\n\nSupercalifragilistic words here."
    print("Width 10:")
    for row in wrap(sample, 10):
        print(repr(row))
    print("Empty input:", wrap("   ", 5))
    print("Done! 🎉")
