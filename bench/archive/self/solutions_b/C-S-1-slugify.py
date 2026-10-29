import re

def slugify(s: str) -> str:
    """
    Lowercase the text; every maximal run of characters that are not 
    ASCII letters or digits becomes a single "-"; no leading or trailing "-".
    """
    # Lowercase the input
    s = s.lower()
    
    # Replace every maximal run of non-ASCII letters or digits with a single "-"
    # [^a-z0-9] matches any character that is not an ASCII lowercase letter or digit
    s = re.sub(r'[^a-z0-9]+', '-', s)
    
    # Remove leading and trailing "-"
    return s.strip('-')
