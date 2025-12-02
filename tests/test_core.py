import unittest
import os
from src.core import identify_type, get_file_signature, load_signatures

class TestCore(unittest.TestCase):
    def setUp(self):
        # Cargar firmas una vez para los tests
        self.signatures = load_signatures()

    def test_identify_png(self):
        # Firma PNG
        result = identify_type("89 50 4E 47 0D 0A 1A 0A", self.signatures)
        self.assertIsNotNone(result)
        self.assertEqual(result['type'], "Imagen PNG")
        
    def test_identify_unknown(self):
        result = identify_type("00 00 00 00", self.signatures)
        self.assertIsNone(result)

    def test_identify_partial_match(self):
        # Debería coincidir si empieza con la firma
        result = identify_type("89 50 4E 47 0D 0A 1A 0A 00 00", self.signatures)
        self.assertIsNotNone(result)
        self.assertEqual(result['type'], "Imagen PNG")

if __name__ == '__main__':
    unittest.main()
