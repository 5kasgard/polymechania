import re


def wrap(text: str, width: int) -> list[str]:
    paragraphs = [p for p in re.split(r'\n[ \t\r\f\v]*\n', text) if p.split()]
    out: list[str] = []
    for pi, para in enumerate(paragraphs):
        if pi > 0:
            out.append("")
        words = para.split()
        line = ""
        for word in words:
            if len(word) > width:
                if line:
                    out.append(line)
                    line = ""
                for i in range(0, len(word), width):
                    out.append(word[i:i + width])
                # the next word always starts a new line after a long word
                line = ""
                continue
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= width:
                line += " " + word
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
    return out
