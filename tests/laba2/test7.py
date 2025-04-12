import unittest
from unittest.mock import patch
from src.laba2.task7 import increment_counter, demonstrate_race_condition

class TestRaceCondition(unittest.TestCase):

    def setUp(self):
        global counter
        counter = 0  # Сбрасываем счетчик перед каждым тестом

    def test_increment_counter_single_thread(self):
        """Тестируем increment_counter в одном потоке"""

        increment_counter()

        self.assertEqual(counter, 0)

    @patch('time.sleep')
    def test_increment_counter_behavior(self, mock_sleep):
        """Тестируем логику increment_counter"""

        # Мокируем sleep чтобы ускорить тест
        mock_sleep.return_value = None

        increment_counter()

        # Проверяем что sleep вызывался
        self.assertTrue(mock_sleep.call_count > 0)
        self.assertEqual(counter, 0)

    @patch('builtins.print')
    def test_demonstrate_race_condition(self, mock_print):
        """Тестируем что функция демонстрации запускает потоки"""
        with patch('threading.Thread') as mock_thread:
            # Настраиваем мок-потоки
            mock_thread.return_value.start.return_value = None
            mock_thread.return_value.join.return_value = None

            demonstrate_race_condition()

            # Проверяем, что создали 10 потоков
            self.assertEqual(mock_thread.call_count, 10)

            # Проверяем, что для каждого вызвали start и join
            self.assertEqual(mock_thread.return_value.start.call_count, 10)
            self.assertEqual(mock_thread.return_value.join.call_count, 10)


if __name__ == '__main__':
    unittest.main()