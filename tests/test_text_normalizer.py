"""
Unit tests for TextNormalizer class.
"""
import unittest
from src.core.text_normalizer import TextNormalizer

class TestTextNormalizer(unittest.TestCase):
    """Test cases for text normalization."""
    
    def setUp(self):
        """Initialize TextNormalizer for each test."""
        self.normalizer = TextNormalizer()
    
    def test_normalize_text_uppercase(self):
        """Test that text is converted to uppercase."""
        text = "José Luis Pérez"
        normalized = self.normalizer.normalize_text(text)
        self.assertEqual(normalized, "JOSE LUIS PEREZ")
    
    def test_normalize_text_remove_special_chars(self):
        """Test removal of special characters."""
        text = "Año 2023 - Proyecto #1"
        normalized = self.normalizer.normalize_text(text)
        self.assertEqual(normalized, "ANO 2023 - PROYECTO _1")
    
    def test_normalize_text_trim_spaces(self):
        """Test trimming of extra spaces."""
        text = "   Nombre   Completo  "
        normalized = self.normalizer.normalize_text(text)
        self.assertEqual(normalized, "NOMBRE COMPLETO")
    
    def test_normalize_text_empty_string(self):
        """Test handling of empty string."""
        text = ""
        normalized = self.normalizer.normalize_text(text)
        self.assertEqual(normalized, "")
    
    def test_normalize_text_with_numbers(self):
        """Test normalization with numbers."""
        text = "Proyecto 123 - Fase 2"
        normalized = self.normalizer.normalize_text(text)
        self.assertEqual(normalized, "PROYECTO 123 - FASE 2")

if __name__ == '__main__':
    unittest.main()
