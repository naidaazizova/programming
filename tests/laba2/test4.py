import asyncio
import unittest
from unittest.mock import patch
import src.laba2.task4 as task4


class TestHTTPRequests(unittest.TestCase):

    @patch('requests.get')  # Мокируем requests.get для тестов
    def test_fetch_sync(self, mock_get):
        # Настроим mock, чтобы он возвращал заданный статус и время ответа
        mock_get.return_value.status_code = 200

        url, duration, status = task4.fetch_sync("https://www.google.com")

        self.assertEqual(status, 200)
        self.assertTrue(duration >= 0)  # Проверяем, что время ответа положительное
        self.assertEqual(url, "https://www.google.com")

    @patch('requests.get')
    def test_run_sync(self, mock_get):
        # Настроим mock, чтобы все запросы возвращали одинаковый результат
        mock_get.return_value.status_code = 200

        results = task4.run_sync()

        self.assertEqual(len(results), 3)  # Проверяем, что все 5 URL обработаны
        for result in results:
            self.assertEqual(result[2], 200)  # Проверяем, что статус 200
            self.assertTrue(result[1] >= 0)  # Время ответа не может быть отрицательным

    @patch('requests.get')
    def test_fetch_async(self, mock_get):
        # Настроим mock для асинхронного запроса
        mock_get.return_value.status_code = 200

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(task4.fetch_async("https://www.google.com"))

        self.assertEqual(result[2], 200)
        self.assertTrue(result[1] >= 0)  # Проверяем, что время ответа не отрицательное
        self.assertEqual(result[0], "https://www.google.com")

    @patch('requests.get')
    def test_run_async(self, mock_get):
        # Настроим mock для всех асинхронных запросов
        mock_get.return_value.status_code = 200

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(task4.run_async())

        self.assertEqual(len(results), 3)  # Проверяем, что все URL обработаны
        for result in results:
            self.assertEqual(result[2], 200)  # Статус 200
            self.assertTrue(result[1] >= 0)  # Время ответа не отрицательное


if __name__ == '__main__':
    unittest.main()