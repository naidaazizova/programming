import unittest
from io import StringIO
import sys
import time
from src.laba1.task1 import logger, example

class TestLoggerDecorator(unittest.TestCase):

    def setUp(self):
        # Перенаправляем вывод в StringIO для перехвата print
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        # Возвращаем стандартный вывод обратно
        sys.stdout = sys.__stdout__

    def test_example_logging(self):
        # Вызываем тестируемую функцию
        result = example(5, 7)

        # Получаем все, что было выведено в stdout
        output = self.held_output.getvalue().strip().split('\n')

        # Проверяем, что вывод включает правильное имя функции
        self.assertIn("Имя функции: example", output[0])

        # Проверяем, что аргументы правильные
        self.assertIn("Аргументы: (5, 7), {}", output[1])

        # Проверяем, что время выполнения указано (приблизительно)
        time_output = output[2]
        self.assertTrue(time_output.startswith("Время выполнения:"))

        # Проверяем, что результат правильный
        self.assertIn("Результат: 12", output[3])

        # Используем assertEqual для проверки, что результат вычисления верный
        self.assertEqual(result, 12)

    def test_empty_arguments(self):
        # Проверяем случай с пустыми аргументами
        result = example(0, 0)

        # Получаем вывод
        output = self.held_output.getvalue().strip().split('\n')

        # Проверяем корректность аргументов
        self.assertIn("Аргументы: (0, 0), {}", output[1])

        # Проверяем результат
        self.assertEqual(result, 0)

    def test_single_argument(self):
        # Проверяем с одним аргументом
        result = example(5, 0)

        output = self.held_output.getvalue().strip().split('\n')

        self.assertIn("Аргументы: (5, 0), {}", output[1])

        # Проверяем результат
        self.assertEqual(result, 5)

    def test_execution_time_logged(self):
        # Засекаем время выполнения теста, чтобы проверить, что декоратор замеряет время
        start_time = time.time()
        example(100, 200)
        end_time = time.time()

        # Получаем вывод, который был напечатан в stdout
        output = self.held_output.getvalue().strip().split('\n')
        time_output = output[2]

        # Проверяем, что декоратор вывел время выполнения
        self.assertTrue(time_output.startswith("Время выполнения:"))

        # Извлекаем время выполнения из вывода и проверяем, что оно не превышает разумный порог
        elapsed_time = float(time_output.split(": ")[1].split()[0])
        self.assertTrue(elapsed_time < (end_time - start_time) + 0.1, "Время выполнения декоратора слишком велико")
        self.assertTrue(elapsed_time >= 0, "Отрицательное время выполнения.")

if __name__ == '__main__':
    unittest.main()
