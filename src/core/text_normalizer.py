"""
Text normalization module for consistent text formatting.
"""
import re
import unicodedata

class TextNormalizer:
    """Class for text normalization operations."""
    
    def __init__(self):
        self._special_chars = {
            '&': 'AND',
            '@': ' ',
            '_': ' ',
            '-': ' ',
            '.': ' ',
            ',': ' ',
            "'": ' ',
            '"': ' ',
        }
        
    def normalize_text(self, text: str) -> str:
        """
        Normalize text by:
        - Converting to uppercase
        - Removing accents
        - Replacing special characters
        - Removing extra spaces
        
        Args:
            text (str): Text to normalize
            
        Returns:
            str: Normalized text
        """
        if not text:
            return ""
            
        # Convert to uppercase
        text = text.upper()
        
        # Remove accents
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ASCII', 'ignore').decode('ASCII')
        
        # Replace special characters
        for char, replacement in self._special_chars.items():
            text = text.replace(char, replacement)
            
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text.strip())
        
        return text
