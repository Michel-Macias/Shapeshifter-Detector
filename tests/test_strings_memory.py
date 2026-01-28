import unittest
import os
from src.core import extract_strings

class TestStringsMemory(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_strings_split.bin"
        # Crear un contenido que fuerce a una cadena a estar en el borde de un bloque de 4096 bytes
        # Llenamos con basura no legible (0x00) y ponemos una palabra clave justo en el límite
        with open(self.test_file, "wb") as f:
            f.write(b"\x00" * 4094) # 4094 bytes nulos
            f.write(b"HOLA_MUNDO")  # 'HO' estará en el fin del primer bloque y 'LA_MUNDO' en el siguiente (si el bloque es 4096)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_extract_strings_split_boundary(self):
        # El test debe detectar 'HOLA_MUNDO' incluso si el bloque de lectura corta la palabra
        strings = extract_strings(self.test_file)
        self.assertIn("HOLA_MUNDO", strings)

if __name__ == '__main__':
    unittest.main()
