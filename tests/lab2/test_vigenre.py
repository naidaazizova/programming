import unittest
from src.lab2.vigenre import encrypt_vigenere, decrypt_vigenere


class MyTestCase(unittest.TestCase):
    def test_vigenre(self):
        self.assertEqual(encrypt_vigenere("PYTHON", "A"), 'PYTHON')
        self.assertEqual(encrypt_vigenere("python", "a"), 'python')
        self.assertEqual(encrypt_vigenere("ATTACKATDAWN", "LEMON"), 'LXFOPVEFRNHR')
        self.assertEqual(decrypt_vigenere("PYTHON", "A"), 'PYTHON')
        self.assertEqual(decrypt_vigenere("python", "a"), 'python')
        self.assertEqual(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"), 'ATTACKATDAWN')


if __name__ == '__main__':
    unittest.main()
