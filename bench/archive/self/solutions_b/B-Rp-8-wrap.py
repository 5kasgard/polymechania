def wrap(text: str, width: int) -> list[str]:
    if not text or text.isspace():
        return []

    # Split into paragraphs by runs of blank lines
    # A blank line is a line that is empty or only whitespace
    import re
    # Split by two or more newlines, or a newline followed by whitespace and another newline
    # However, the spec says "runs of one or more blank lines".
    # Let's split by lines first to identify blank lines.
    lines = text.splitlines()
    
    paragraphs_raw = []
    current_para_lines = []
    
    for line in lines:
        if line.strip() == "":
            if current_para_lines:
                paragraphs_raw.append(" ".join(current_para_lines))
                current_para_lines = []
            # We don't add empty strings to paragraphs_raw yet, 
            # we just use them as delimiters.
        else:
            current_para_lines.append(line.strip())
    if current_para_lines:
        paragraphs_raw.append(" ".join(current_para_lines))

    # Re-evaluating paragraph splitting: 
    # "split text into paragraphs at runs of one or more blank lines"
    # This means the text is divided by the gaps.
    
    # Let's use a more robust approach for paragraph splitting
    # Find indices of blank lines
    all_lines = text.split('\n')
    para_indices = []
    is_blank = [line.strip() == "" for line in all_lines]
    
    paragraphs_of_words = []
    current_words = []
    
    i = 0
    while i < len(all_lines):
        if is_blank[i]:
            if current_words:
                paragraphs_of_words.append(current_words)
                current_words = []
            # Skip the run of blank lines
            while i < len(all_lines) and is_blank[i]:
                i += 1
        else:
            # Add words from this non-blank line
            words_in_line = all_lines[i].split()
            current_words.extend(words_in_line)
            i += 1
    if current_words:
        paragraphs_of_words.append(current_words)

    if not paragraphs_of_words:
        return []

    result_paragraphs = []
    
    for words in paragraphs_of_words:
        lines_in_para = []
        current_line = []
        current_len = 0
        
        for word in words:
            w_len = len(word)
            
            # Case 1: Word is longer than width
            if w_len > width:
                # If there's a current line, finish it
                if current_line:
                    lines_in_para.append(" ".join(current_line))
                    current_line = []
                    current_len = 0
                
                # Break the long word
                for j in range(0, w_len, width):
                    chunk = word[j : j + width]
                    if len(chunk) == width:
                        lines_in_para.append(chunk)
                    else:
                        # Last piece
                        current_line = [chunk]
                        current_len = len(chunk)
                
                # If the last chunk was a full width, current_line is empty
                # If it was a partial chunk, it's in current_line
                if not current_line and lines_in_para and lines_in_para[-1] == word[len(word)-width:]:
                    # This logic is slightly flawed, let's simplify.
                    pass 
                # Let's restart the long word logic cleanly.
                continue # Handled below

            # Case 2: Word fits in current line
            # space needed if current_line is not empty
            space = 1 if current_line else 0
            if current_len + space + w_len <= width:
                current_line.append(word)
                current_len += space + w_len
            else:
                # Start new line
                lines_in_para.append(" ".join(current_line))
                current_line = [word]
                current_len = w_len
        
        # Re-implementing word loop to handle long words correctly
        lines_in_para = []
        current_line = []
        current_len = 0
        
        for word in words:
            if len(word) > width:
                # Flush current line
                if current_line:
                    lines_in_para.append(" ".join(current_line))
                    current_line = []
                    current_len = 0
                # Split word
                for j in range(0, len(word), width):
                    chunk = word[j : j + width]
                    if len(chunk) == width:
                        lines_in_para.append(chunk)
                    else:
                        # Last piece starts a new line
                        current_line = [chunk]
                        current_len = len(chunk)
            else:
                space = 1 if current_line else 0
                if current_len + space + len(word) <= width:
                    current_line.append(word)
                    current_len += space + len(word)
                else:
                    lines_in_para.append(" ".join(current_line))
                    current_line = [word]
                    current_len = len(word)
        
        if current_line:
            lines_in_para.append(" ".join(current_line))
            
        result_paragraphs.append("\n".join(lines_in_para))

    # The spec says: "Paragraphs are separated by one empty string "" in the output."
    # This implies if we have 2 paragraphs, the list is [p1, "", p2]
    final_output = []
    for i, p in enumerate(result_paragraphs):
        final_output.append(p)
        if i < len(result_paragraphs) - 1:
            final_output.append("")
            
    return final_output

if __name__ == '__main__':
    print(f"Test 1: {wrap('Hello world\n\nThis is a test', 5)}")
    print(f"Test 2: {wrap('Supercalifragilisticexpialidocious', 5)}")
    print(f"Test 3: {wrap('   ', 10)}")
