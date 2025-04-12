import unittest
from unittest.mock import patch, MagicMock, call
import time
import threading
from src.laba2.task6 import print_message, sequential_execution, parallel_execution

class TestThreadingFunctions(unittest.TestCase):

    @patch('time.sleep')
    @patch('builtins.print')
    def test_print_message(self, mock_print, mock_sleep):
        """Тестируем функцию print_message"""
        test_msg = "Test message"
        test_delay = 3

        print_message(test_msg, test_delay)

        mock_sleep.assert_called_once_with(test_delay)
        mock_print.assert_called_once_with(test_msg)

    @patch('src.laba2.task6.print_message')
    @patch('time.time')
    def test_sequential_execution(self, mock_time, mock_print):
        """Тестируем sequential_execution"""
        # Настраиваем мок для time.time
        mock_time.side_effect = [0, 6.0]  # start_time, end_time

        # Мокируем print_message, чтобы не ждать реальных задержек
        mock_print.return_value = None

        sequential_execution()

        # Проверяем, что print_message вызывалась 3 раза
        self.assertEqual(mock_print.call_count, 3)

        # Проверяем переданные аргументы
        expected_calls = [
            call("Сообщение 1", 2),
            call("Сообщение 2", 2),
            call("Сообщение 3", 2)
        ]
        mock_print.assert_has_calls(expected_calls)

    @patch('threading.Thread')
    @patch('time.time')
    def test_parallel_execution(self, mock_time, mock_thread):
        """Тестируем parallel_execution"""
        # Настраиваем мок для time.time
        mock_time.side_effect = [0, 2.0]  # start_time, end_time

        # Создаем мок-потоки
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        parallel_execution()

        # Проверяем, что Thread создавался 3 раза
        self.assertEqual(mock_thread.call_count, 3)

        # Проверяем что для каждого потока вызывались start и join
        self.assertEqual(mock_thread_instance.start.call_count, 3)
        self.assertEqual(mock_thread_instance.join.call_count, 3)

    @patch('builtins.print')
    def test_output_order(self, mock_print):
        """Тестируем порядок вывода в parallel_execution"""
        with patch('threading.Thread') as mock_thread:
            # Настраиваем мок-поток для вызова реальной функции
            def thread_side_effect(target, args):
                target(*args)
                return MagicMock()

            mock_thread.side_effect = thread_side_effect

            parallel_execution()

            # Проверяем, что все сообщения были выведены
            output_messages = [call[0][0] for call in mock_print.call_args_list]
            self.assertIn("Поток 1", output_messages)
            self.assertIn("Поток 2", output_messages)
            self.assertIn("Поток 3", output_messages)


if __name__ == '__main__':
    unittest.main()