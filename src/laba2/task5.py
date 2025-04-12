import threading
import time

def print_with_delay(message):
    """Функция печати строки с задержкой"""
    time.sleep(2)
    print(message)

def main():
    # Создаем и запускаем поток
    thread = threading.Thread(target=print_with_delay, args=("Сообщение из потока после задержки 2 сек",))
    thread.start()

    print("Основной поток продолжает работу")
    thread.join()  # Ожидаем завершениe потока
    print("Все потоки завершены")


if __name__ == '__main__':
    main()