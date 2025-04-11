import time
def logger(show_magic=False):
    def decorator(cls):
        def wrap_method(method):
            def wrapped(*args, **kwargs):
                # Получаем информацию о вызове
                class_name = cls.__name__
                method_name = method.__name__

                print(f"Имя: {class_name}.{method_name}")
                print(f"Аргументы:{args[1:]}, {kwargs}")

                start_t = time.time()
                result = method(*args, **kwargs)
                duration = time.time() - start_t

                print(f"Время выполнения: {duration:.6f} сек")
                print(f"Результат: {result}")
                print("-" * 30)

                return result
            return wrapped

        # Оборачиваем методы класса
        for name, method in cls.__dict__.items():
            if callable(method):
                # Проверяем, нужно ли логировать магические методы
                is_magic = name.startswith('__') and name.endswith('__')
                if not is_magic or show_magic:
                    setattr(cls, name, wrap_method(method))

        return cls
    return decorator

@logger(show_magic=True)
class MyClass:
    def __init__(self, value):
        self.value = value

    def add(self, x, y):
        return x + y

    def __str__(self):
        return f"MyClass with value: {self.value}"


obj = MyClass(10)  # __init__ будет залогирован
print(obj.add(5, 8))  # add будет залогирован
print(str(obj))  # __str__ будет залогирован