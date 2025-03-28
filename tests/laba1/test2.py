import unittest
from io import StringIO
import sys
from unittest.mock import patch
import random
from src.laba1.task2 import retry, risk

class TestRetryDecorator(unittest.TestCase):
    def setUp(self):
        # Перенаправляем вывод в StringIO для перехвата print
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        # Возвращаем стандартный вывод обратно
        sys.stdout = sys.__stdout__
        random.seed()

    def test_success_on_first_attempt(self):
        # Фиксируем random, чтобы функция всегда возвращала успех
        with patch('random.random', return_value=0.97):
            result = risk()
            self.assertEqual(result, "Успешно!")

        # Проверяем, что не было сообщений о повторных попытках
        output = self.held_output.getvalue()
        self.assertEqual(output, "")

    def test_retry_structure(self):
        random_returns = [0.1, 0.4, 0.97]  # первые два < 0.9, третий > 0.9
        with patch('random.random', side_effect=random_returns):
            result = risk()
            self.assertEqual(result, "Успешно!")

        # Проверяем сообщения о повторных попытках
        output = self.held_output.getvalue().split('\n')
        self.assertIn('Попытка 1 не удалась, подождите 1 секунд перед следующей попыткой', output[0])
        self.assertIn('Попытка 2 не удалась, подождите 1 секунд перед следующей попыткой', output[1])
        self.assertEqual(len(output), 3)  # 2 сообщения + пустая строка

    def test_all_attempts_are_failed(self):
        # Все попытки вернут значение < 0.9 (вызовут исключение)
        with patch('random.random', return_value=0.1):
            result = risk()
            self.assertIsNone(result)

        # Проверяем сообщения о неудачных попытках
        output = self.held_output.getvalue().split('\n')
        self.assertIn('Попытка 1 не удалась, подождите 1 секунд перед следующей попыткой', output[0])
        self.assertIn('Попытка 2 не удалась, подождите 1 секунд перед следующей попыткой', output[1])
        self.assertIn('Все 3 попыток(-ки) не удались', output[2])

    def test_only_special_exceptions(self):
        """Тест обработки только указанных исключений"""

        # Создадим тестовую функцию с декоратором
        @retry(attempts=2, delay=0.1, exceptions=(ValueError,))
        def test_func():
            raise TypeError("Исключение является не обрабатываемым")

        # Проверяем, что исключение пробрасывается сразу
        with self.assertRaises(TypeError):
            test_func()

        # Проверяем, что не было попыток повтора
        output = self.held_output.getvalue()
        self.assertEqual(output, "")

if __name__ == '__main__':
    unittest.main()