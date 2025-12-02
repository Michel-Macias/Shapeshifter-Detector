import unittest
import os
from src.core import identify_type, get_file_signature

class TestCore(unittest.TestCase):
    def test_identify_png(self):
        # PNG signature
        self.assertEqual(identify_type("89 50 4E 47 0D 0A 1A 0A"), "PNG Image")
        
    def test_identify_unknown(self):
        self.assertEqual(identify_type("00 00 00 00"), "Unknown File Type")

    def test_identify_partial_match(self):
        # Should match if it starts with the signature
        self.assertEqual(identify_type("89 50 4E 47 0D 0A 1A 0A 00 00"), "PNG Image")

if __name__ == '__main__':
    unittest.main()
