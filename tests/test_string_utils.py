import unittest
from string_utils import reverse, capitalize_words, count_vowels

class TestStringUtils(unittest.TestCase):
    
    def test_reverse(self):
        self.assertEqual(reverse("hello"), "olleh")
        self.assertEqual(reverse(""), "")
        self.assertEqual(reverse("a"), "a")
    
    def test_capitalize_words(self):
        self.assertEqual(capitalize_words("hello world"), "Hello World")
        self.assertEqual(capitalize_words("python code"), "Python Code")
        self.assertEqual(capitalize_words(""), "")
    
    def test_count_vowels(self):
        self.assertEqual(count_vowels("hello"), 2)
        self.assertEqual(count_vowels("why"), 1)
        self.assertEqual(count_vowels("sky"), 0)
        self.assertEqual(count_vowels(""), 0)
    
    def test_validation(self):
        with self.assertRaises(TypeError):
            reverse(123)
        with self.assertRaises(TypeError):
            capitalize_words(None)
        with self.assertRaises(TypeError):
            count_vowels([])

if __name__ == "__main__":
    unittest.main()