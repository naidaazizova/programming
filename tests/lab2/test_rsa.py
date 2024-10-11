import unittest
from src.lab2.rsa import is_prime, gcd, multiplicative_inverse, generate_keypair, encrypt, decrypt

class MyTestCase(unittest.TestCase):
    def test_isprime(self):
        self.assertTrue(is_prime(2)) # add assertion here
        self.assertTrue(is_prime(11))
        self.assertFalse(is_prime(8))
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(4))

    def test_gcd(self): #нахождение наибольшего общего делителя
        self.assertEqual(gcd(12, 15), 3)
        self.assertEqual(gcd(3, 7), 1)
        self.assertEqual(gcd(3, 0), 3)
        self.assertEqual(gcd(0, 3), 3)

    def test_multiplicative_inverse(self): #нахождение мультипликативного обратного
        self.assertEqual(multiplicative_inverse(7, 40), 23)
        self.assertEqual(multiplicative_inverse(3, 11), 4)


    def test_generate_keypair(self):  #тестирование генерации ключей
        public_key, private_key = generate_keypair(71, 73)
        self.assertEqual(public_key[0] * private_key[0] % ((71 - 1) * (73 - 1)), 1)
        #проверяем, что d * e = 1 (mod phi(n))

    def test_encrypt_decrypt(self): #тесты шифрования и расшифровки
        p, q = 71, 73
        public_key, private_key = generate_keypair(p, q)
        message = "HELLO WORLD"
        encrypted = encrypt(private_key, message)
        decrypted = decrypt(public_key, encrypted)
        self.assertEqual(message, decrypted) #тут проверяем, чтобы расшифрованное сообщение совпадало с исходным














if __name__ == '__main__':
    unittest.main()
