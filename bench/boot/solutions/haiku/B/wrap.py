def wrap(text: str, width: int) -> list[str]:
    def wrap_words(words: list[str], width: int) -> list[str]:
        lines: list[str] = []
        current = ""
        for word in words:
            if len(word) > width:
                if current:
                    lines.append(current)
                    current = ""
                for start in range(0, len(word), width):
                    lines.append(word[start:start + width])
            elif not current:
                current = word
            elif len(current) + 1 + len(word) <= width:
                current += " " + word
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    paragraphs: list[list[str]] = []
    current_words: list[str] = []
    for line in text.split("\n"):
        if line.strip() == "":
            if current_words:
                paragraphs.append(current_words)
                current_words = []
        else:
            current_words.extend(line.split())
    if current_words:
        paragraphs.append(current_words)

    out: list[str] = []
    for i, words in enumerate(paragraphs):
        if i > 0:
            out.append("")
        out.extend(wrap_words(words, width))
    return out
