import threading
import time

counter = 0
counter_lock = threading.Lock()  # Создаем объект блокировки

def reset_counter():
    global counter
    counter = 0

def increment_counter():
    global counter
    for _ in range(100000):
        with counter_lock:  # Блокируем доступ к shared ресурсу
            # Критическая секция (атомарная операция)
            temp = counter
            time.sleep(0.000001)  # Искусственная задержка
            counter = temp + 1

def demonstrate_race_condition():
    global counter
    reset_counter()

    threads = []
    for _ in range(10):
        thread = threading.Thread(target=increment_counter)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Ожидаемое: 1000000, Полученное: {counter}")

if __name__ == '__main__':
    print("Демонстрация с блокировкой:")
    for i in range(5):
        demonstrate_race_condition()