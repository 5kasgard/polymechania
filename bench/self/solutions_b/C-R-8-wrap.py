def wrap(text: str, width: int) -> list[str]:
    if not text or text.isspace():
        return []

    # Split into paragraphs by runs of one or more blank lines
    import re
    # Split by one or more lines that are empty or only whitespace
    # We use a regex that looks for a newline followed by optional whitespace and another newline
    # Or just start/end of string.
    # A simpler way: split by '\n' and identify empty/whitespace lines.
    
    raw_lines = text.splitlines()
    paragraphs_raw = []
    current_para_lines = []
    
    for line in raw_lines:
        if not line.strip():
            if current_para_lines:
                paragraphs_raw.append(current_para_lines)
                current_para_lines = []
        else:
            current_para_lines.append(line)
    if current_para_lines:
        paragraphs_raw.append(current_para_lines)

    if not paragraphs_raw:
        return []

    result = []
    for i, para_lines in enumerate(paragraphs_raw):
        # Extract all words from the paragraph
        words = []
        for line in para_lines:
            words.extend(line.split())
        
        if not words:
            # This case shouldn't happen based on the split logic, 
            # but for safety:
            if i < len(paragraphs_raw) - 1:
                result.append("")
            continue

        para_lines_wrapped = []
        idx = 0
        while idx < len(words):
            word = words[idx]
            
            # Case 1: Word is longer than width
            if len(word) > width:
                # If we were building a line, finish it
                # (But the spec says "A word longer than width always starts a new line")
                # This implies we don't append it to a current line.
                
                # Cut the word
                for j in range(0, len(word), width):
                    para_lines_wrapped.append(word[j : j + width])
                idx += 1
            else:
                # Case 2: Word fits in width
                # Greedy fill
                current_line = []
                current_len = 0
                
                while idx < len(words):
                    w = words[idx]
                    # Check if word fits in width
                    if len(w) > width:
                        # Cannot include this word in current line
                        break
                    
                    # Calculate length if added: current_len + space + len(w)
                    space = 1 if current_len > 0 else 0
                    if current_len + space + len(w) <= width:
                        current_line.append(w)
                        current_len += space + len(w)
                        idx += 1
                    else:
                        # Word doesn't fit
                        break
                
                if current_line:
                    para_lines_wrapped.append(" ".join(current_line))
        
        result.extend(para_lines_wrapped)
        
        # Add separator if not the last paragraph
        if i < len(paragraphs_raw) - 1:
            result.append("")

    return result
