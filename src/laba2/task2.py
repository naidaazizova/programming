import asyncio

async def delayed_message(delay: int, message: str) -> None:
    """Асинхронная функция, которая ждёт delay секунд и выводит message."""
    await asyncio.sleep(delay)
    print(message)

async def main():
    # Создаем три задачи с разными задержками
    task1 = delayed_message(2, "Сообщение после 2 секунд")
    task2 = delayed_message(1, "Сообщение после 1 секунды")
    task3 = delayed_message(3, "Сообщение после 3 секунд")

    # Запускаем все задачи одновременно
    await asyncio.gather(task1, task2, task3)

    print("Все сообщения выведены")

# Запускаем асинхронную программу
asyncio.run(main())