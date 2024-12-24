"""
Text normalization module.
"""
import re
import unicodedata

class TextNormalizer:
    """Class for normalizing text."""
    
    def normalize_text(self, text: str) -> str:
        """Normalize text by removing accents and special characters.
        
        Args:
            text: Text to normalize
            
        Returns:
            Normalized text
        """
        # First, convert to uppercase
        text = text.upper()
        
        # Remove accents
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ASCII', 'ignore').decode('ASCII')
        
        # Normalize multiple spaces and trim
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Replace specific punctuation
        text = text.replace(',', '')
        text = text.replace('.', '_')
        
        # Replace other special characters with underscore
        text = re.sub(r'[^A-Z0-9\s\-_]', '_', text)
        
        # Normalize multiple consecutive underscores or hyphens
        text = re.sub(r'[_\-]+', '-', text)
        
        # Trim leading/trailing hyphens or underscores
        text = text.strip('-_')
        
        return text
