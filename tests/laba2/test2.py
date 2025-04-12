import asyncio
import unittest
from unittest.mock import patch
from src.laba2.task2 import delayed_message, main


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_delayed_message(self):
        """Тестируем функцию delayed_message"""

        async def run_test():
            with patch('asyncio.sleep') as mock_sleep:
                mock_sleep.return_value = asyncio.Future()
                mock_sleep.return_value.set_result(None)

                with patch('builtins.print') as mock_print:
                    await delayed_message(1, "test")
                    mock_sleep.assert_called_once_with(1)
                    mock_print.assert_called_once_with("test")

        self.loop.run_until_complete(run_test())


    def test_gather_concurrent_execution(self):
        """Проверяем, что задачи выполняются конкурентно"""

        async def run_test():
            start_time = self.loop.time()
            await main()
            end_time = self.loop.time()

            # Общее время должно быть ~3 секунды (макс задержка), а не 6 секунд (сумма задержек)
            self.assertAlmostEqual(end_time - start_time, 3, delta=0.2)

        self.loop.run_until_complete(run_test())

    def test_all_messages_printed(self):
        """Проверяем, что все сообщения выводятся"""

        async def run_test():
            with patch('builtins.print') as mock_print:
                await main()

                # Проверяем что все 3 сообщения были напечатаны
                self.assertEqual(mock_print.call_count, 4)  # 3 сообщения + финальное
                calls = [call[0][0] for call in mock_print.call_args_list]
                self.assertIn("Сообщение после 1 секунды", calls)
                self.assertIn("Сообщение после 2 секунд", calls)
                self.assertIn("Сообщение после 3 секунд", calls)
                self.assertIn("Все сообщения выведены", calls)

        self.loop.run_until_complete(run_test())


if __name__ == '__main__':
    unittest.main()
