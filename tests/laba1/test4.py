import unittest
from io import StringIO
import sys
from src.laba1.task4 import call_limiter

class TestCallLimiter(unittest.TestCase):
    def setUp(self):
        # Создаем тестовый класс с декоратором
        @call_limiter(limit=2)
        class TestClass:
            def method1(self):
                return "method1 called"

            def method2(self, x):
                return x * 2

            def __str__(self):
                return "magic method"

        self.TestClass = TestClass
        self.obj = TestClass()

    def test_allowed_calls(self):
        """Тест разрешенных вызовов в пределах лимита"""
        # Первые два вызова должны работать
        self.assertEqual(self.obj.method1(), "method1 called")
        self.assertEqual(self.obj.method1(), "method1 called")

        # Метод с аргументами
        self.assertEqual(self.obj.method2(5), 10)
        self.assertEqual(self.obj.method2(3), 6)

    def test_exceed_limit(self):
        """Тест превышения лимита вызовов"""
        # Два разрешенных вызова
        self.obj.method1()
        self.obj.method1()

        # Третий вызов должен вызвать исключение
        with self.assertRaises(RuntimeError) as context:
            self.obj.method1()

        self.assertEqual(str(context.exception), "Метод method1 можно вызвать не более 2 раз")

    def test_separate_method_counters(self):
        """Тест отдельных счетчиков для разных методов"""
        # Исчерпываем лимит для method1
        self.obj.method1()
        self.obj.method1()

        # method2 должен работать, у него свой счетчик
        self.assertEqual(self.obj.method2(10), 20)
        self.assertEqual(self.obj.method2(2), 4)

        # Проверяем, что method1 все еще заблокирован
        with self.assertRaises(RuntimeError):
            self.obj.method1()

    def test_magic_methods_unlimited(self):
        """Тест, что магические методы не ограничиваются"""
        # __str__ можно вызывать сколько угодно раз
        self.assertEqual(str(self.obj), "magic method")
        self.assertEqual(str(self.obj), "magic method")
        self.assertEqual(str(self.obj), "magic method")

    def test_separate_instances(self):
        """Тест, что разные экземпляры имеют отдельные счетчики"""
        obj2 = self.TestClass()

        # Исчерпываем лимит для первого объекта
        self.obj.method1()
        self.obj.method1()

        # Второй объект должен иметь свои счетчики
        self.assertEqual(obj2.method1(), "method1 called")
        self.assertEqual(obj2.method1(), "method1 called")

        # Проверяем, что лимит работает для каждого объекта отдельно
        with self.assertRaises(RuntimeError):
            self.obj.method1()

        with self.assertRaises(RuntimeError):
            obj2.method1()


if __name__ == '__main__':
    unittest.main()