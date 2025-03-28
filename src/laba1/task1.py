import time

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Имя функции: {func.__name__}")
        print(f"Аргументы: {args}, {kwargs}")

        start_t = time.time()
        result = func(*args, **kwargs)
        end_t = time.time()

        print(f"Время выполнения: {end_t - start_t:.6f} секунд")
        print(f"Результат: {result}")

        return result
    return wrapper

@logger
def example(x, y):
    return x + y

example(4, 5)