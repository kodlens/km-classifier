import re
import unicodedata

def slugify(text: str) -> str:
    # Normalize (remove accents, etc.)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    
    # Lowercase, remove non-alphanumeric except spaces
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text.lower())
    
    # Replace spaces/dashes with single dash
    text = re.sub(r"[\s-]+", "-", text).strip("-")
    
    return text