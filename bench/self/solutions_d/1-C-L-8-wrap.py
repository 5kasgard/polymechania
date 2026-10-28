def wrap(text: str, width: int) -> list[str]:
    lines_out: list[str] = []
    paragraphs: list[list[str]] = []
    current: list[str] = []
    for raw in text.splitlines():
        if raw.strip() == "":
            if current:
                paragraphs.append(current)
                current = []
        else:
            current.append(raw)
    if current:
        paragraphs.append(current)

    for p_index, para_lines in enumerate(paragraphs):
        if p_index > 0:
            lines_out.append("")
        words = " ".join(para_lines).split()
        line = ""
        for word in words:
            if len(word) > width:
                if line:
                    lines_out.append(line)
                    line = ""
                for start in range(0, len(word), width):
                    lines_out.append(word[start:start + width])
                continue
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= width:
                line = line + " " + word
            else:
                lines_out.append(line)
                line = word
        if line:
            lines_out.append(line)
    return lines_out


if __name__ == '__main__':
    print("👋 Hello from the wrap demo!")
    sample = "The quick brown fox jumps over the lazy dog.\n\nSupercalifragilistic is long.\n"
    for width in (10, 15):
        print(f"🔹 width={width}")
        for row in wrap(sample, width):
            print(repr(row))
    print("✅ Done!")
