def wrap(text: str, width: int) -> list[str]:
    # Split into paragraphs at runs of blank (empty or whitespace-only) lines.
    paragraphs = []
    current = []
    for line in text.splitlines():
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

        line = ""
        for word in words:
            if len(word) > width:
                # Flush whatever is pending, then cut the long word.
                if line:
                    output.append(line)
                    line = ""
                pieces = [word[i:i + width] for i in range(0, len(word), width)]
                for piece in pieces[:-1]:
                    output.append(piece)
                # The last piece may still accept following words.
                line = pieces[-1]
            elif not line:
                line = word
            elif len(line) + 1 + len(word) <= width:
                line += " " + word
            else:
                output.append(line)
                line = word
        if line:
            output.append(line)

    return output


if __name__ == '__main__':
    sample = "The quick brown fox jumps over the lazy dog.\n\nSupercalifragilistic words here."
    for row in wrap(sample, 12):
        print(repr(row))
    print(wrap("   \n  ", 5))  # expect []
