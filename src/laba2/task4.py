import requests
import asyncio
import time

URLS = [
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.stackoverflow.com"
]

# Синхронный запрос
def fetch_sync(url):
    start = time.time()
    response = requests.get(url)
    end = time.time()
    return url, round(end - start, 2), response.status_code

def run_sync():
    print("=== Синхронные запросы ===")
    start = time.time()
    results = []
    for url in URLS:
        result = fetch_sync(url)
        results.append(result)
        print(f"{result[0]} ответил за {result[1]}с, статус: {result[2]}")
    total = round(time.time() - start, 2)
    print(f"Общее время выполнения: {total}с\n")
    return results


# Асинхронные запросы через потоки
async def fetch_async(url):
    loop = asyncio.get_running_loop()
    start = time.time()
    result = await loop.run_in_executor(None, fetch_sync, url)
    end = time.time()
    return result

async def run_async():
    print("=== Асинхронные запросы (через потоки) ===")
    start = time.time()
    tasks = [fetch_async(url) for url in URLS]
    results = await asyncio.gather(*tasks)
    for url, duration, status in results:
        print(f"{url} ответил за {duration}с, статус: {status}")
    total = round(time.time() - start, 2)
    print(f"Общее время выполнения: {total}с\n")
    return results


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async())
