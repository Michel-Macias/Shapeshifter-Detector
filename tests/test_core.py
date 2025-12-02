import unittest
import os
from src.core import identify_type, get_file_signature, load_signatures, calculate_hashes, calculate_entropy, extract_strings

class TestCore(unittest.TestCase):
    def setUp(self):
        self.signatures = load_signatures()
        # Crear archivo temporal para tests
        with open("temp_test_file.txt", "w") as f:
            f.write("Hola Mundo Forense")

    def tearDown(self):
        if os.path.exists("temp_test_file.txt"):
            os.remove("temp_test_file.txt")

    def test_identify_png(self):
        result = identify_type("89 50 4E 47 0D 0A 1A 0A", self.signatures)
        self.assertIsNotNone(result)
        self.assertEqual(result['type'], "Imagen PNG")
        
    def test_hashes(self):
        hashes = calculate_hashes("temp_test_file.txt")
        self.assertIsNotNone(hashes)
        self.assertTrue("md5" in hashes)
        self.assertTrue("sha256" in hashes)

    def test_entropy(self):
        entropy = calculate_entropy("temp_test_file.txt")
        self.assertGreaterEqual(entropy, 0.0)
        self.assertLessEqual(entropy, 8.0)

    def test_strings(self):
        strings = extract_strings("temp_test_file.txt")
        self.assertIn("Hola Mundo Forense", strings)

if __name__ == '__main__':
    unittest.main()
