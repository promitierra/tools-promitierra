"""
Comprehensive unit tests for TextNormalizer class.
"""
import unittest
import random
import string
from src.core.text_normalizer import TextNormalizer

class TestTextNormalizer(unittest.TestCase):
    """Comprehensive test suite for TextNormalizer."""
    
    def setUp(self):
        """Initialize TextNormalizer for each test."""
        self.normalizer = TextNormalizer()
    
    def _generate_random_string(self, length=10, include_special_chars=False):
        """Generate a random string for testing."""
        chars = string.ascii_letters + string.digits
        if include_special_chars:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def test_basic_normalization(self):
        """Test basic text normalization."""
        test_cases = [
            ("Hello World", "HELLO WORLD"),
            ("  Trimmed  Spaces  ", "TRIMMED SPACES"),
            ("múltiplé áccents", "MULTIPLE ACCENTS"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input=input_text):
                normalized = self.normalizer.normalize_text(input_text)
                self.assertEqual(normalized, expected)
    
    def test_special_characters(self):
        """Test handling of special characters."""
        test_cases = [
            ("Hello, World!", "HELLO WORLD"),
            ("File.name", "FILE_NAME"),
            ("User#123", "USER_123"),
            ("Special@Chars", "SPECIAL_CHARS"),
            ("Dash-Separated", "DASH-SEPARATED"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input=input_text):
                normalized = self.normalizer.normalize_text(input_text)
                self.assertEqual(normalized, expected)
    
    def test_complex_names(self):
        """Test normalization of complex names and IDs."""
        test_cases = [
            ("1515 15 - LUI S FER NANDO", "1515 15 - LUIS FERNANDO"),
            ("  Juan   Manuel   Pérez  ", "JUAN MANUEL PEREZ"),
            ("1.515.15 - Luis, Fernando", "1_515_15 - LUIS FERNANDO"),
            ("  1515 15 . LUI S , FER NANDO  ", "1515 15 - LUIS FERNANDO"),
            ("Juan2 Pérez3", "JUAN2 PEREZ3"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input=input_text):
                normalized = self.normalizer.normalize_text(input_text)
                self.assertEqual(normalized, expected)
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        test_cases = [
            ("", ""),  # Empty string
            ("   ", ""),  # Only whitespace
            ("a" * 1000, "A" * 1000),  # Very long string
            ("!@#$%^&*()", ""),  # Only special characters
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input=input_text):
                normalized = self.normalizer.normalize_text(input_text)
                self.assertEqual(normalized, expected)
    
    def test_unicode_characters(self):
        """Test handling of Unicode characters."""
        test_cases = [
            ("Café", "CAFE"),
            ("Señor", "SENOR"),
            ("Año Nuevo", "ANO NUEVO"),
            ("こんにちは", ""),  # Non-Latin characters
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input=input_text):
                normalized = self.normalizer.normalize_text(input_text)
                self.assertEqual(normalized, expected)
    
    def test_random_input_robustness(self):
        """Test robustness with random input."""
        for _ in range(100):  # Run 100 random tests
            # Generate random strings with and without special characters
            random_str = self._generate_random_string(
                length=random.randint(1, 50), 
                include_special_chars=random.choice([True, False])
            )
            
            try:
                normalized = self.normalizer.normalize_text(random_str)
                # Basic assertions
                self.assertTrue(isinstance(normalized, str))
                self.assertTrue(all(c.isalnum() or c in '-_' for c in normalized))
            except Exception as e:
                self.fail(f"Unexpected error with input '{random_str}': {e}")
    
    def test_performance(self):
        """Basic performance test for normalization."""
        import timeit
        
        # Test normalization time for a moderately long string
        long_string = " ".join([self._generate_random_string() for _ in range(10)])
        
        def normalize_test():
            self.normalizer.normalize_text(long_string)
        
        # Ensure normalization takes less than 0.01 seconds
        execution_time = timeit.timeit(normalize_test, number=1000) / 1000
        self.assertLess(execution_time, 0.01, 
            "Normalization is taking too long. Consider optimizing.")

if __name__ == '__main__':
    unittest.main()
