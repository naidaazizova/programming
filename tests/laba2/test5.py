import unittest
from unittest.mock import patch, MagicMock, call
from src.laba2.task5 import print_with_delay, main

class TestThreadingExample(unittest.TestCase):

    @patch('time.sleep')
    @patch('builtins.print')
    def test_print_with_delay(self, mock_print, mock_sleep):
        """Тестируем функцию print_with_delay"""
        test_message = "Test message"

        print_with_delay(test_message)

        mock_sleep.assert_called_once_with(2)
        mock_print.assert_called_once_with(test_message)

    @patch('threading.Thread')
    def test_main_creates_thread(self, mock_thread):
        """Тестируем, что main создает и запускает поток"""
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        main()

        mock_thread.assert_called_once_with(
            target=print_with_delay,
            args=("Сообщение из потока после задержки 2 сек",)
        )
        mock_thread_instance.start.assert_called_once()
        mock_thread_instance.join.assert_called_once()

    @patch('builtins.print')
    def test_main_output(self, mock_print):
        """Тестируем вывод main"""
        # Создаем реальный поток, но мокируем sleep в print_with_delay
        with patch('src.laba2.task5.time.sleep'):
            main()

        # Проверяем вывод основного потока
        self.assertIn(call("Основной поток продолжает работу"), mock_print.call_args_list)
        self.assertIn(call("Все потоки завершены"), mock_print.call_args_list)

        # Проверяем, что сообщение из потока было напечатано
        thread_calls = [c for c in mock_print.call_args_list
                        if c[0][0] == "Сообщение из потока после задержки 2 сек"]
        self.assertEqual(len(thread_calls), 1)


if __name__ == '__main__':
    unittest.main()
