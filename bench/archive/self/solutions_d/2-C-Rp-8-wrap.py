def wrap(text: str, width: int) -> list[str]:
    # Split into paragraphs: runs of blank lines separate them.
    paragraphs: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.strip() == "":
            if current:
                paragraphs.append(current)
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append(current)

    output: list[str] = []
    for p_index, para in enumerate(paragraphs):
        if p_index > 0:
            output.append("")
        words = " ".join(para).split()
        line = ""
        for word in words:
            if len(word) > width:
                if line:
                    output.append(line)
                    line = ""
                for start in range(0, len(word), width):
                    output.append(word[start:start + width])
                continue
            if not line:
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
    print(wrap(sample, 10))
    print(wrap("", 5))
    print(wrap("abcdefghij klm", 4))
