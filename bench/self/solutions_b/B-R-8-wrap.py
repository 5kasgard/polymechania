def wrap(text: str, width: int) -> list[str]:
    if not text or text.isspace():
        return []

    # Split into paragraphs by runs of one or more blank lines
    # A blank line is a line that is empty or only whitespace
    raw_paragraphs = []
    current_para_lines = []
    
    lines = text.splitlines()
    for line in lines:
        if not line.strip():
            if current_para_lines:
                raw_paragraphs.append(" ".join(current_para_lines))
                current_para_lines = []
            else:
                # This handles multiple blank lines between paragraphs
                pass
        else:
            current_para_lines.append(line.strip())
    
    if current_para_lines:
        raw_paragraphs.append(" ".join(current_para_lines))

    # If the text was just whitespace but splitlines didn't catch it
    if not raw_paragraphs:
        return []

    result = []
    for i, para in enumerate(raw_paragraphs):
        words = para.split()
        if not words:
            continue
            
        para_lines = []
        current_line = []
        current_len = 0
        
        for word in words:
            w_len = len(word)
            
            # Case 1: Word is longer than width
            if w_len > width:
                # If there is a pending line, flush it
                if current_line:
                    para_lines.append(" ".join(current_line))
                    current_line = []
                    current_len = 0
                
                # Break the long word into pieces
                for j in range(0, w_len, width):
                    piece = word[j : j + width]
                    # If this is the last piece of the word, it might be the end of a line
                    # but the spec says "each piece on its own line"
                    para_lines.append(piece)
                # The next word starts a new line, so we don't add to current_line
                continue

            # Case 2: Word fits in current line (including space)
            # Space needed if current_line is not empty
            space_needed = 1 if current_line else 0
            if current_len + space_needed + w_len <= width:
                current_line.append(word)
                current_len += space_needed + w_len
            else:
                # Case 3: Word doesn't fit, start new line
                para_lines.append(" ".join(current_line))
                current_line = [word]
                current_len = w_len
        
        if current_line:
            para_lines.append(" ".join(current_line))
            
        result.extend(para_lines)
        
        # Add empty string separator between paragraphs
        if i < len(raw_paragraphs) - 1:
            result.append("")

    return result
