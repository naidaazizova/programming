def call_limiter(limit):
    def decorator(cls):
        class Wrapped(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._call_counts = {}  # Словарь для хранения счетчиков вызовов методов

            def __getattribute__(self, name):
                attr = super().__getattribute__(name)
                if callable(attr) and name not in ['__init__', '__class__', '_call_counts']:
                    if name not in self._call_counts:
                        self._call_counts[name] = 0

                    def wrapped(*args, **kwargs):
                        if self._call_counts[name] >= limit:
                            raise RuntimeError(f"Метод {name} можно вызвать не более {limit} раз")
                        self._call_counts[name] += 1
                        return attr(*args, **kwargs)

                    return wrapped
                return attr
        return Wrapped
    return decorator

@call_limiter(limit=2)
class MyClass:
    def method1(self):
        print("Метод 1 вызван")

    def method2(self):
        print("Метод 2 вызван")

    def __str__(self):
        return "Строковое представление"


obj = MyClass()
obj.method1()
obj.method1()
try:
    obj.method1()  # Вызовет исключение
except RuntimeError as e:
    print(e)

obj.method2()
print(str(obj))