import unittest
import asyncio
from unittest.mock import patch
from src.laba2.task1 import delayed_message

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_message_output(self):
        """Проверяет, что сообщение выводится после задержки."""

        async def run_test():
            with unittest.mock.patch('builtins.print') as mock_print:
                await delayed_message(1, "Test message")
                mock_print.assert_called_once_with("Test message")

        self.loop.run_until_complete(run_test())

    def test_delay_execution(self):
        """Проверяет, что функция действительно ожидает указанное время."""

        async def run_test():
            with unittest.mock.patch('asyncio.sleep') as mock_sleep:
                mock_sleep.return_value = asyncio.Future()
                mock_sleep.return_value.set_result(None)

                await delayed_message(2, "Any message")
                mock_sleep.assert_called_once_with(2)

        self.loop.run_until_complete(run_test())

    def test_concurrent_execution_order(self):
        """Проверяет порядок выполнения при конкурентных вызовах."""

        async def run_test():
            results = []

            async def collect_message(delay, msg):
                await delayed_message(delay, msg)
                results.append(msg)

            task1 = asyncio.create_task(collect_message(0.2, "Second"))
            task2 = asyncio.create_task(collect_message(0.1, "First"))

            await asyncio.gather(task1, task2)
            self.assertEqual(results, ["First", "Second"])

        self.loop.run_until_complete(run_test())

    def test_zero_delay(self):
        """Проверяет работу с нулевой задержкой."""

        async def run_test():
            with unittest.mock.patch('builtins.print') as mock_print:
                await delayed_message(0, "Instant message")
                mock_print.assert_called_once_with("Instant message")

        self.loop.run_until_complete(run_test())

if __name__ == '__main__':
    unittest.main()
