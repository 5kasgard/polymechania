def wrap(text: str, width: int) -> list[str]:
    # Split into paragraphs at runs of blank (whitespace-only) lines.
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
                # Flush any line in progress, then cut the long word.
                if line:
                    output.append(line)
                    line = ""
                for i in range(0, len(word), width):
                    output.append(word[i:i + width])
                # The next word must start a new line.
                continue
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= width:
                line = line + " " + word
            else:
                output.append(line)
                line = word
        if line:
            output.append(line)

    return output


if __name__ == '__main__':
    sample = "The quick brown fox jumps over the lazy dog\n\n\nSupercalifragilistic words here"
    for row in wrap(sample, 10):
        print(repr(row))
