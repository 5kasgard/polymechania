def wrap(text: str, width: int) -> list[str]:
    # Split into paragraphs: runs of blank (whitespace-only) lines separate them.
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

    out: list[str] = []
    for pi, para_lines in enumerate(paragraphs):
        if pi > 0:
            out.append("")
        words = " ".join(para_lines).split()
        line = ""
        for word in words:
            if len(word) > width:
                # Flush the current line, then chop the long word.
                if line:
                    out.append(line)
                    line = ""
                for start in range(0, len(word), width):
                    out.append(word[start:start + width])
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


if __name__ == '__main__':
    sample = "The quick brown fox jumps over the lazy dog.\n\nSupercalifragilistic word.\n\n\nEnd."
    for w in (10, 15):
        print(f"width={w}")
        for row in wrap(sample, w):
            print(repr(row))
        print()
    print(wrap("   \n  ", 5))  # expect []
