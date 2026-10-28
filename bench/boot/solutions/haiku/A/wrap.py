def wrap(text: str, width: int) -> list[str]:
    # Group the text into paragraphs: runs of non-blank lines separated by blank lines.
    paragraphs = []
    current_lines = []
    for line in text.split("\n"):
        if line.strip() == "":
            if current_lines:
                paragraphs.append(current_lines)
                current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        paragraphs.append(current_lines)

    output = []
    for p_index, para_lines in enumerate(paragraphs):
        if p_index > 0:
            output.append("")

        words = " ".join(para_lines).split()
        out_lines = []
        cur = ""
        for word in words:
            if len(word) > width:
                if cur:
                    out_lines.append(cur)
                    cur = ""
                for start in range(0, len(word), width):
                    out_lines.append(word[start:start + width])
            elif cur == "":
                cur = word
            elif len(cur) + 1 + len(word) <= width:
                cur = cur + " " + word
            else:
                out_lines.append(cur)
                cur = word
        if cur:
            out_lines.append(cur)

        output.extend(out_lines)

    return output
