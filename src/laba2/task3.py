import asyncio

async def delayed_message(delay: int, message: str) -> str:
    """Асинхронная функция, которая ждёт delay секунд и возвращает message."""
    await asyncio.sleep(delay)
    return message

async def main():
    # Создаем список корутин с разными параметрами
    tasks = [
        delayed_message(2, "Сообщение после 2 секунд"),
        delayed_message(1, "Сообщение после 1 секунды"),
        delayed_message(3, "Сообщение после 3 секунд")
    ]

    # Обрабатываем задачи по мере их завершения
    for completed_task in asyncio.as_completed(tasks):
        message = await completed_task
        print(message)

    print("Все сообщения выведены")

# Запускаем асинхронную программу
asyncio.run(main())