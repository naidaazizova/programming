import unittest
import threading
from src.laba2.task8 import reset_counter, increment_counter
import src.laba2.task8 as task8


class TestCounterWithThreads(unittest.TestCase):

    def test_reset_counter(self):
        task8.counter = 12345
        reset_counter()
        self.assertEqual(task8.counter, 0, "Сброс счетчика не работает корректно")

    def test_increment_with_lock(self):
        reset_counter()

        threads = []
        for _ in range(10):
            thread = threading.Thread(target=increment_counter)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(task8.counter, 1000000, f"Счетчик должен быть 1000000, но равен {task8.counter}")

    def test_multiple_runs_consistency(self):
        """Тест на многократный запуск для гарантии детерминированного результата"""
        for _ in range(3):
            reset_counter()
            threads = [
                threading.Thread(target=increment_counter)
                for _ in range(10)
            ]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            self.assertEqual(task8.counter, 1000000, f"Ожидалось 1000000, но получили {task8.counter}")


if __name__ == '__main__':
    unittest.main()
