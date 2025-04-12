import unittest
import asyncio
from unittest.mock import patch
from src.laba2.task3 import delayed_message, main


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Создаем новый event loop для каждого теста
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        # Закрываем loop после каждого теста
        self.loop.close()

    def test_delayed_message_returns_correct_value(self):
        """Тест проверяет, что функция возвращает правильное сообщение"""

        async def run_test():
            result = await delayed_message(1, "test message")
            self.assertEqual(result, "test message")

        self.loop.run_until_complete(run_test())

    def test_delayed_message_calls_sleep(self):
        """Тест проверяет, что функция вызывает asyncio.sleep"""

        async def run_test():
            with patch('asyncio.sleep') as mock_sleep:
                mock_sleep.return_value = asyncio.Future()
                mock_sleep.return_value.set_result(None)

                await delayed_message(2, "test")
                mock_sleep.assert_called_once_with(2)

        self.loop.run_until_complete(run_test())


    def test_main_completes_all_tasks(self):
        """Тест проверяет, что все задачи завершаются"""

        async def run_test():
            with patch('asyncio.sleep') as mock_sleep:
                mock_sleep.return_value = asyncio.Future()
                mock_sleep.return_value.set_result(None)

                await main()

                # Проверяем что нет незавершенных задач
                pending = [t for t in asyncio.all_tasks(self.loop) if not t.done()]
                self.assertEqual(len(pending), 1)

        self.loop.run_until_complete(run_test())


if __name__ == '__main__':
    unittest.main()