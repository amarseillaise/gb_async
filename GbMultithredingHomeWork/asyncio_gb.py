import asyncio
import time
from random import randint


def gen_numbers_list(length: int):
    return [randint(1, 100) for _ in range(length)]


async def summarize(arr: list):
    return sum(arr)


async def main():
    start_time = time.time()

    tasks = []
    chunk_size = 1
    numbers_list = gen_numbers_list(1000000)

    async with asyncio.TaskGroup() as tg:
        for i in range(0, len(numbers_list), chunk_size):
            chunk = numbers_list[i:i + chunk_size]
            task = tg.create_task(summarize(chunk))
            tasks.append(task)

    summ = sum([task.result() for task in tasks])

    print(f'result is {summ}. Time elapsed: {time.time() - start_time:2f}')

if __name__ == '__main__':
    asyncio.run(main())
