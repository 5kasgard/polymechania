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

    result = []
    for p_index, para_lines in enumerate(paragraphs):
        if p_index > 0:
            result.append("")
        words = " ".join(para_lines).split()
        line = ""
        for word in words:
            if len(word) > width:
                # Flush the current line, then cut the long word into pieces.
                if line:
                    result.append(line)
                    line = ""
                for start in range(0, len(word), width):
                    result.append(word[start:start + width])
                continue
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= width:
                line += " " + word
            else:
                result.append(line)
                line = word
        if line:
            result.append(line)
    return result


if __name__ == '__main__':
    sample = "The quick brown fox jumps over the lazy dog.\n\nSupercalifragilistic words wrap here."
    for out_line in wrap(sample, 12):
        print(repr(out_line))
    print(wrap("", 5))
    print(wrap("abcdefghijkl mn", 5))
