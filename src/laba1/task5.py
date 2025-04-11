import asyncio

async def first_function():
    print("Функция 1 - первый вывод")
    await asyncio.sleep(1)
    print("Функция 1 - второй вывод")
    await asyncio.sleep(4)
    print("Функция 1 - третий вывод")

async def second_function():
    print("Функция 2 - первый вывод")
    await asyncio.sleep(3)
    print("Функция 2 - второй вывод")
    await asyncio.sleep(1)
    print("Функция 2 - третий вывод")
    await asyncio.sleep(1)
    print("Функция 2 - четвертый вывод")

async def main():
    # Запускаем обе функции одновременно
    await asyncio.gather(
        first_function(),
        second_function()
    )

# Запуск асинхронного кода
asyncio.run(main())