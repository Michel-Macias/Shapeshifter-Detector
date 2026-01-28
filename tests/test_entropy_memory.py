import unittest
import os
import math
from src.core import calculate_entropy

class TestEntropyMemory(unittest.TestCase):
    def setUp(self):
        # Crear un archivo de prueba con contenido repetitivo y conocido
        # 1024 caracteres 'A' y 1024 caracteres 'B'
        # Entropía esperada: 1.0 (ya que solo hay dos símbolos equiprobables)
        self.test_file = "test_entropy_large.bin"
        with open(self.test_file, "wb") as f:
            f.write(b"A" * 1024)
            f.write(b"B" * 1024)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_calculate_entropy_accuracy(self):
        # La entropía de una distribución 50/50 de dos símbolos es exactamente 1.0
        entropy = calculate_entropy(self.test_file)
        self.assertAlmostEqual(entropy, 1.0, places=5)

    def test_calculate_entropy_empty_file(self):
        empty_file = "empty.bin"
        with open(empty_file, "wb") as f:
            pass
        entropy = calculate_entropy(empty_file)
        os.remove(empty_file)
        self.assertEqual(entropy, 0.0)

if __name__ == '__main__':
    unittest.main()
