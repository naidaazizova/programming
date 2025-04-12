import asyncio

async def delayed_message(delay: int, message: str) -> None:
    """Асинхронная функция, которая ждёт delay секунд и выводит message."""
    await asyncio.sleep(delay)
    print(message)

async def main():
    print("Начало")
    await delayed_message(2, "Сообщение после 2 секунд")
    print("Продолжение")
    await delayed_message(1, "Еще одно сообщение после 1 секунды")
    print("Завершение")

# Запускаем асинхронную программу
asyncio.run(main())


