import random
import time

def retry(attempts, delay, exceptions=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if exceptions is not None and type(e) not in exceptions:
                        raise
                    if attempt < attempts:
                        print(f'Попытка {attempt} не удалась, подождите {delay} секунд перед следующей попыткой')
                        time.sleep(delay)
            print(f'Все {attempts} попыток(-ки) не удались')
        return wrapper
    return decorator

@retry(attempts=3, delay=1)
def risk():
    if random.random() < 0.9:
        raise ValueError
    return "Успешно!"

risk()