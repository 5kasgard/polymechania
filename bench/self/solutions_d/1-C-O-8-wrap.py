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

    output = []
    for p_index, para_lines in enumerate(paragraphs):
        if p_index > 0:
            output.append("")
        words = " ".join(para_lines).split()

        lines = []
        cur = ""
        for word in words:
            if len(word) > width:
                # Close the current line, then cut the long word into pieces.
                if cur:
                    lines.append(cur)
                    cur = ""
                pieces = [word[i:i + width] for i in range(0, len(word), width)]
                for piece in pieces[:-1]:
                    lines.append(piece)
                # The last piece is the start of the current line; the
                # next word will try to join it, so it may be kept open.
                cur = pieces[-1]
            elif not cur:
                cur = word
            elif len(cur) + 1 + len(word) <= width:
                cur = cur + " " + word
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        output.extend(lines)

    return output


if __name__ == "__main__":
    sample = "The quick brown fox jumps over the lazy dog.\n\nAbcdefghijklmnop qr"
    print("🦊 Wrapped at width 12:")
    for line in wrap(sample, 12):
        print(repr(line))
    print("✅ Empty input gives:", wrap("   \n  ", 5))
