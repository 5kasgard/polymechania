def wrap(text: str, width: int) -> list[str]:
    if not text or text.isspace():
        return []

    # Split text into lines to identify paragraph boundaries
    lines = text.splitlines()
    paragraphs_raw = []
    current_paragraph_lines = []

    for line in lines:
        if line.strip() == "":
            if current_paragraph_lines:
                paragraphs_raw.append(" ".join(current_paragraph_lines))
                current_paragraph_lines = []
            else:
                # If we have multiple blank lines, we still only care about the split
                pass
        else:
            current_paragraph_lines.append(line.strip())
    
    if current_paragraph_lines:
        paragraphs_raw.append(" ".join(current_paragraph_lines))

    # If the text was just blank lines, paragraphs_raw might be empty
    if not paragraphs_raw:
        return []

    # Re-evaluating paragraph splitting: the spec says "split text into paragraphs 
    # at runs of one or more blank lines". 
    # Let's use a more robust approach for paragraph splitting.
    
    import re
    # Split by one or more lines that are empty or only whitespace
    # We use a regex that matches a newline followed by optional whitespace and another newline
    # or start/end of string.
    
    # Actually, a simpler way:
    raw_paragraphs = []
    current_p = []
    
    # Split by actual newline characters
    all_lines = text.split('\n')
    for line in all_lines:
        if line.strip() == "":
            if current_p:
                raw_paragraphs.append(current_p)
                current_p = []
        else:
            current_p.append(line)
    if current_p:
        raw_paragraphs.append(current_p)

    if not raw_paragraphs:
        return []

    final_output = []
    
    for i, p_lines in enumerate(raw_paragraphs):
        # Extract words from the paragraph
        words = []
        for line in p_lines:
            words.extend(line.split())
        
        if not words:
            continue

        p_wrapped_lines = []
        current_line = ""

        for word in words:
            if len(word) > width:
                # If there's a current line being built, finish it
                if current_line:
                    p_wrapped_lines.append(current_line)
                    current_line = ""
                
                # Break the long word into pieces
                for j in range(0, len(word), width):
                    chunk = word[j:j+width]
                    # If this is not the last chunk, it must be exactly width
                    # If it is the last chunk, it might be shorter.
                    # But the spec says: "each piece on its own line"
                    p_wrapped_lines.append(chunk)
                # The next word starts a new line, so we don't set current_line
                continue

            # Try to add word to current line
            if not current_line:
                current_line = word
            else:
                if len(current_line) + 1 + len(word) <= width:
                    current_line += " " + word
                else:
                    p_wrapped_lines.append(current_line)
                    current_line = word
        
        if current_line:
            p_wrapped_lines.append(current_line)
            
        final_output.append(p_wrapped_lines)

    # Flatten the output with "" between paragraphs
    result = []
    for i, p_lines in enumerate(final_output):
        result.extend(p_lines)
        if i < len(final_output) - 1:
            result.append("")
            
    return result
