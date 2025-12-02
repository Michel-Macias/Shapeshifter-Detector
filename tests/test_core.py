import unittest
import os
from src.core import identify_type, get_file_signature

class TestCore(unittest.TestCase):
    def test_identify_png(self):
        # Firma PNG
        self.assertEqual(identify_type("89 50 4E 47 0D 0A 1A 0A"), "Imagen PNG")
        
    def test_identify_unknown(self):
        self.assertEqual(identify_type("00 00 00 00"), "Tipo de Archivo Desconocido")

    def test_identify_partial_match(self):
        # Debería coincidir si empieza con la firma
        self.assertEqual(identify_type("89 50 4E 47 0D 0A 1A 0A 00 00"), "Imagen PNG")

if __name__ == '__main__':
    unittest.main()
