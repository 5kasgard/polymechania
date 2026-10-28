import re


def wrap(text: str, width: int) -> list[str]:
    if not text or not text.strip():
        return []

    # Paragraphs are separated by one or more blank (whitespace-only) lines.
    paragraphs = re.split(r"\n[ \t\r\f\v]*(?:\n[ \t\r\f\v]*)+", text)

    output: list[str] = []
    emitted_paragraph = False

    for para in paragraphs:
        words = para.split()
        if not words:
            continue

        if emitted_paragraph:
            output.append("")
        emitted_paragraph = True

        lines: list[str] = []
        current = ""
        for word in words:
            if len(word) > width:
                # Flush the current line, then cut the long word into pieces.
                if current:
                    lines.append(current)
                    current = ""
                for start in range(0, len(word), width):
                    lines.append(word[start:start + width])
                continue

            if not current:
                current = word
            elif len(current) + 1 + len(word) <= width:
                current = current + " " + word
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)

        output.extend(lines)

    return output


if __name__ == "__main__":
    sample = "The quick brown fox jumps over the lazy dog.\n\nSupercalifragilistic words wrap nicely! 🎉"
    for line in wrap(sample, 12):
        print(repr(line))
