def wrap(text: str, width: int) -> list[str]:
    # Split into paragraphs at runs of blank lines (empty or whitespace-only).
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

    result: list[str] = []
    for p_index, para_lines in enumerate(paragraphs):
        if p_index > 0:
            result.append("")
        words = " ".join(para_lines).split()

        line = ""
        for word in words:
            if len(word) > width:
                # Close the current line, then cut the long word into chunks.
                if line:
                    result.append(line)
                    line = ""
                for start in range(0, len(word), width):
                    result.append(word[start:start + width])
                continue
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= width:
                line = line + " " + word
            else:
                result.append(line)
                line = word
        if line:
            result.append(line)

    return result


if __name__ == '__main__':
    print(wrap("the quick brown fox jumps over the lazy dog", 10))
    print(wrap("abcdefghijklmnop qr", 5))
    print(wrap("first paragraph here\n\n\nsecond one", 8))
    print(wrap("   \n  ", 4))
