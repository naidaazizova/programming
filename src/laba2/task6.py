import threading
import time

def print_message(message, delay):
    """Функция печати сообщения с задержкой"""
    time.sleep(delay)
    print(message)

def sequential_execution():
    """Последовательное выполнение"""
    print("\nПоследовательное выполнение:")
    start_time = time.time()

    print_message("Сообщение 1", 2)
    print_message("Сообщение 2", 2)
    print_message("Сообщение 3", 2)

    duration = time.time() - start_time
    print(f"Общее время: {duration:.2f} сек")


def parallel_execution():
    """Параллельное выполнение в потоках"""
    print("\nПараллельное выполнение:")
    start_time = time.time()

    # Создаем потоки
    thread1 = threading.Thread(target=print_message, args=("Поток 1", 2))
    thread2 = threading.Thread(target=print_message, args=("Поток 2", 2))
    thread3 = threading.Thread(target=print_message, args=("Поток 3", 2))

    # Запускаем потоки
    thread1.start()
    thread2.start()
    thread3.start()

    # Ожидаем завершения всех потоков
    thread1.join()
    thread2.join()
    thread3.join()

    duration = time.time() - start_time
    print(f"Общее время: {duration:.2f} сек")

if __name__ == '__main__':
    sequential_execution()
    parallel_execution()