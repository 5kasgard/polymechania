def wrap(text: str, width: int) -> list[str]:
    if not text or text.isspace():
        return []

    # Split text into paragraphs by runs of blank lines
    # A blank line is a line that is empty or only whitespace
    import re
    # We split by one or more lines that consist only of whitespace
    # Using a regex to find sequences of newline(s) with optional whitespace between them
    # but the spec says "runs of one or more blank lines".
    # Let's split by lines first to identify them.
    lines = text.splitlines()
    
    paragraphs_raw = []
    current_para_lines = []
    
    for line in lines:
        if line.strip() == "":
            if current_para_lines:
                paragraphs_raw.append(current_para_lines)
                current_para_lines = []
        else:
            current_para_lines.append(line)
    if current_para_lines:
        paragraphs_raw.append(current_para_lines)

    if not paragraphs_raw:
        return []

    all_wrapped_lines = []
    
    for i, para_lines in enumerate(paragraphs_raw):
        # Extract all words from the paragraph
        words = []
        for line in para_lines:
            words.extend(line.split())
        
        if not words:
            # This case shouldn't happen with the current split logic, 
            # but for safety:
            para_wrapped = []
        else:
            # Process words and handle long words
            processed_words = []
            for w in words:
                if len(w) <= width:
                    processed_words.append(w)
                else:
                    # Cut word into pieces of exactly width
                    for j in range(0, len(w), width):
                        processed_words.append(w[j : j + width])
            
            # Greedy line filling
            para_wrapped = []
            if processed_words:
                current_line = []
                current_len = 0
                
                for pw in processed_words:
                    # If pw is a piece of a long word, it must be on its own line
                    # The spec says: "A word longer than width always starts a new line 
                    # and is cut into pieces... each piece on its own line; the next word starts a new line."
                    # This implies pieces of long words cannot be combined with anything else.
                    
                    # Let's re-evaluate: "A word longer than width... each piece on its own line; 
                    # the next word starts a new line."
                    # This means if a word was long, its pieces are isolated.
                    
                    # Let's refine the word processing to distinguish "normal" words 
                    # from "long word pieces".
                    pass

            # Re-implementing word processing to strictly follow the "long word" rule
            para_wrapped = []
            words_to_fill = []
            # We need to know if a word was originally long
            # Let's use a list of (is_piece, content)
            word_units = []
            for w in words:
                if len(w) <= width:
                    word_units.append((False, w))
                else:
                    for j in range(0, len(w), width):
                        word_units.append((True, w[j : j + width]))
            
            idx = 0
            while idx < len(word_units):
                is_piece, content = word_units[idx]
                if is_piece:
                    # Each piece on its own line, next word starts a new line
                    para_wrapped.append(content)
                    idx += 1
                else:
                    # Normal word: greedy fill
                    line_buffer = [content]
                    line_len = len(content)
                    idx += 1
                    while idx < len(word_units):
                        next_is_piece, next_content = word_units[idx]
                        if next_is_piece:
                            # Cannot add a piece to a line with a normal word
                            break
                        
                        # Check if adding next_content + space fits
                        if line_len + 1 + len(next_content) <= width:
                            line_buffer.append(next_content)
                            line_len += 1 + len(next_content)
                            idx += 1
                        else:
                            break
                    para_wrapped.append(" ".join(line_buffer))
            
            if not para_wrapped:
                para_wrapped = []

        all_wrapped_lines.extend(para_wrapped)
        
        # Add empty string between paragraphs
        if i < len(paragraphs_raw) - 1:
            all_wrapped_lines.append("")

    return all_wrapped_lines

if __name__ == '__main__':
    # Demo 1: Basic wrapping
    print(f"Demo 1: {wrap('Hello world! This is a test.', 10)}")
    
    # Demo 2: Long words
    print(f"Demo 2: {wrap('Supercalifragilisticexpialidocious', 5)}")
    
    # Demo 3: Paragraphs
    print(f"Demo 3: {wrap('Para one.\n\nPara two.', 10)}")
    
    # Demo 4: Empty/Whitespace
    print(f"Demo 4: {wrap('   ', 5)}")
