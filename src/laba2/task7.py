import threading
import time

counter = 0

def increment_counter():
    global counter
    for _ in range(100000):
        # Имитируем работу, увеличивающую вероятность гонки
        temp = counter
        time.sleep(0.000001)  # Искусственная задержка
        counter = temp + 1

def demonstrate_race_condition():
    global counter
    counter = 0

    threads = []
    for _ in range(10):  # Создаём 10 потоков для усиления эффекта
        thread = threading.Thread(target=increment_counter)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Ожидаемое: 1000000, Полученное: {counter}")

if __name__ == '__main__':
    print("Демонстрация проблемы гонки данных:")
    for i in range(5):
        demonstrate_race_condition()