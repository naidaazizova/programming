import unittest
from io import StringIO
import sys
import time
from unittest.mock import patch
from src.laba1.task3 import logger

class TestLoggerDecorator(unittest.TestCase):
    def setUp(self):
        # Перехватываем вывод в консоль
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        # Восстанавливаем стандартный вывод
        sys.stdout = self.original_stdout

    def test_regular_method_logging(self):
        """Тестируем логирование обычного метода"""

        @logger(show_magic=True)
        class TestClass:
            def test_method(self, a, b):
                return a * b

        obj = TestClass()
        result = obj.test_method(3, 4)

        # Проверяем результат выполнения
        self.assertEqual(result, 12)

        # Проверяем вывод в консоль
        output = self.held_output.getvalue()
        self.assertIn("Имя: TestClass.test_method", output)
        self.assertIn("Аргументы:(3, 4), {}", output)
        self.assertIn("Результат: 12", output)

    def test_magic_method_logging(self):
        """Тестируем логирование магического метода при show_magic=True"""

        @logger(show_magic=True)
        class TestClass:
            def __str__(self):
                return "Test instance"

        obj = TestClass()
        result = str(obj)

        self.assertEqual(result, "Test instance")

        output = self.held_output.getvalue()
        self.assertIn("Имя: TestClass.__str__", output)
        self.assertIn("Результат: Test instance", output)

    def test_magic_method_no_logging(self):
        """Тестируем отсутствие логирования магических методов при show_magic=False"""

        @logger(show_magic=False)
        class TestClass:
            def __str__(self):
                return "No logging"

        obj = TestClass()
        result = str(obj)

        self.assertEqual(result, "No logging")

        output = self.held_output.getvalue()
        self.assertNotIn("Имя: TestClass.__str__", output)

    def test_execution_time(self):
        """Тест измерения времени выполнения"""

        @logger(show_magic=True)
        class TestClass:
            def sleep_method(self, seconds):
                time.sleep(seconds)
                return "done"

        # Используем mock для time.sleep чтобы ускорить тест
        with patch('time.sleep'):
            obj = TestClass()
            obj.sleep_method(0.1)

        # Проверяем что время было измерено и выведено
        output = self.held_output.getvalue()
        self.assertIn("Время выполнения", output)

if __name__ == '__main__':
    unittest.main()
