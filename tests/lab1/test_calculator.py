import unittest
from src.lab1.calculator import calc

class CalculatorTestCase(unittest.TestCase):

    # Тест для проверки работы, можно удалить
    def test_lab1(self):
        self.assertEqual(calc(10, 20, '+'), 30.0)
        self.assertEqual(calc(1000, 5689, '+'), 6689.0)
        self.assertEqual(calc(15, 8, '-'), 7.0)
        self.assertEqual(calc(4, 7, '*'), 28)
        self.assertEqual(calc(0, 4, '*'), 0)
        self.assertEqual(calc(48, 6, '/'), 8.0)
        self.assertEqual(calc(5400, 0, '/'),'Ошибка! Делить на ноль нельзя!')