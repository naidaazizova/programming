import unittest
import asyncio
from io import StringIO
import sys
from src.laba1.task5 import first_function, second_function, main

class TestAsyncFunctions(unittest.TestCase):
    def setUp(self):
        # Перехватываем вывод в консоль
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

        # Создаем новую event loop для каждого теста
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        # Восстанавливаем стандартный вывод
        sys.stdout = self.original_stdout
        self.held_output.close()

        # Закрываем event loop
        self.loop.close()

    async def run_async_test(self, coro):
        """Вспомогательная функция для запуска корутин в тестах"""
        return await coro

    def test_first_function_output(self):
        """Тестируем вывод первой функции"""
        # Запускаем первую функцию
        self.loop.run_until_complete(self.run_async_test(first_function()))

        # Проверяем вывод
        output = self.held_output.getvalue()
        self.assertIn("Функция 1 - первый вывод", output)
        self.assertIn("Функция 1 - второй вывод", output)
        self.assertIn("Функция 1 - третий вывод", output)

    def test_second_function_output(self):
        """Тестируем вывод второй функции"""
        # Запускаем вторую функцию
        self.loop.run_until_complete(self.run_async_test(second_function()))

        # Проверяем вывод
        output = self.held_output.getvalue()
        self.assertIn("Функция 2 - первый вывод", output)
        self.assertIn("Функция 2 - второй вывод", output)
        self.assertIn("Функция 2 - третий вывод", output)
        self.assertIn("Функция 2 - четвертый вывод", output)

    def test_functions_run_concurrently(self):
        """Тестируем конкурентное выполнение функций"""

        async def run_both():
            await asyncio.gather(
                first_function(),
                second_function()
            )

        # Запускаем обе функции вместе
        self.loop.run_until_complete(self.run_async_test(run_both()))

        # Проверяем что вывод перемешан (доказательство конкурентности)
        output = self.held_output.getvalue()
        lines = output.strip().split('\n')

        # Первые два сообщения должны быть от обеих функций
        self.assertTrue(
            {"Функция 1 - первый вывод", "Функция 2 - первый вывод"} == {lines[0], lines[1]}
        )

    def test_first_function_timing(self):
        """Тестируем временные задержки первой функции"""

        async def test_timing():
            start = asyncio.get_event_loop().time()
            await first_function()
            end = asyncio.get_event_loop().time()
            return end - start

        duration = self.loop.run_until_complete(self.run_async_test(test_timing()))
        # Ожидаемое время: 1 + 4 = 5 секунд ± погрешность
        self.assertAlmostEqual(duration, 5.0, delta=0.5)

    def test_second_function_timing(self):
        """Тестируем временные задержки второй функции"""

        async def test_timing():
            start = asyncio.get_event_loop().time()
            await second_function()
            end = asyncio.get_event_loop().time()
            return end - start

        duration = self.loop.run_until_complete(self.run_async_test(test_timing()))
        # Ожидаемое время: 3 + 1 + 1 = 5 секунд ± погрешность
        self.assertAlmostEqual(duration, 5.0, delta=0.5)


if __name__ == '__main__':
    unittest.main()