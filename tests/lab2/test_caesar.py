import unittest
from src.lab2.caesar import encrypt_caesar, decrypt_caesar

class MyTestCase(unittest.TestCase):
    def test_caesar(self):
        self.assertEqual(encrypt_caesar("PYTHON", 3), 'SBWKRQ')
        self.assertEqual(encrypt_caesar("python", 3), 'sbwkrq')
        self.assertEqual(encrypt_caesar("Python3.6", 3), 'Sbwkrq3.6')
        self.assertEqual(encrypt_caesar("", 3), '')
        self.assertEqual(decrypt_caesar("SBWKRQ", 3), 'PYTHON')
        self.assertEqual(decrypt_caesar("sbwkrq", 3), 'python')
        self.assertEqual(decrypt_caesar("Sbwkrq3.6", 3), 'Python3.6')
        self.assertEqual(decrypt_caesar("", 3), '')


if __name__ == '__main__':
    unittest.main()
