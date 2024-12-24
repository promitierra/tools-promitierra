"""
Tests for text normalizer module
"""
import unittest
from src.core.text_normalizer import TextNormalizer

class TestTextNormalizer(unittest.TestCase):
    """Test cases for TextNormalizer class"""
    
    def setUp(self):
        self.normalizer = TextNormalizer()
        
    def test_normalize_text_with_accents(self):
        """Test text normalization with accented characters"""
        test_cases = [
            ("José Pérez", "JOSE PEREZ"),
            ("María Ángeles", "MARIA ANGELES"),
            ("Ñoño", "NONO"),
        ]
        for input_text, expected in test_cases:
            self.assertEqual(
                self.normalizer.normalize_text(input_text),
                expected
            )
            
    def test_normalize_text_with_special_chars(self):
        """Test text normalization with special characters"""
        test_cases = [
            ("John@Doe", "JOHN DOE"),
            ("Smith & Sons", "SMITH AND SONS"),
            ("O'Connor", "O CONNOR"),
        ]
        for input_text, expected in test_cases:
            self.assertEqual(
                self.normalizer.normalize_text(input_text),
                expected
            )
            
    def test_normalize_text_with_multiple_spaces(self):
        """Test text normalization with multiple spaces"""
        test_cases = [
            ("John   Doe", "JOHN DOE"),
            (" James  Bond ", "JAMES BOND"),
            ("Multiple     Spaces", "MULTIPLE SPACES"),
        ]
        for input_text, expected in test_cases:
            self.assertEqual(
                self.normalizer.normalize_text(input_text),
                expected
            )
            
if __name__ == '__main__':
    unittest.main()
