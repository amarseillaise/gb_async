import threading
import time
from random import randint

summ = 0


def gen_numbers_list(length: int):
    return [randint(1, 100) for _ in range(length)]


def summarize(arr: list):
    global summ
    summ += sum(arr)


def main():
    global summ
    start_time = time.time()

    threads = []
    chunk_size = 1000
    numbers_list = gen_numbers_list(1000000)

    for i in range(0, len(numbers_list), chunk_size):
        chunk = numbers_list[i:i + chunk_size]
        thread = threading.Thread(target=summarize, args=(chunk,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f'result is {summ}. Time elapsed: {time.time() - start_time:2f}')


if __name__ == '__main__':
    main()
