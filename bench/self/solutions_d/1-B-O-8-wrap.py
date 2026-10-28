def wrap(text: str, width: int) -> list[str]:
    # Split into paragraphs at runs of blank (whitespace-only) lines.
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
    for p_index, para_lines in enumerate(paragraphs):
        if p_index > 0:
            out.append("")
        words = " ".join(para_lines).split()
        line = ""
        for word in words:
            if len(word) > width:
                if line:
                    out.append(line)
                    line = ""
                # Cut the long word into exact-width pieces.
                pos = 0
                while len(word) - pos > width:
                    out.append(word[pos:pos + width])
                    pos += width
                line = word[pos:]
            else:
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


if __name__ == "__main__":
    sample = "The quick brown fox jumps over the lazy dog."
    print("Width 10:")
    for row in wrap(sample, 10):
        print(repr(row))

    print("\nLong word, width 4:")
    for row in wrap("abcdefghij kl", 4):
        print(repr(row))

    print("\nTwo paragraphs, width 12:")
    for row in wrap("first para here\n\n\nsecond one", 12):
        print(repr(row))
