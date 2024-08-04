import multiprocessing
import time
from random import randint

summ = multiprocessing.Value('i', 0)


def gen_numbers_list(length: int):
    return [randint(1, 100) for _ in range(length)]


def summarize(arr: list, summ):
    with summ.get_lock():
        summ.value += sum(arr)


def main():
    global summ
    start_time = time.time()

    processes = []
    chunk_size = 10000
    numbers_list = gen_numbers_list(1000000)

    for i in range(0, len(numbers_list), chunk_size):
        chunk = numbers_list[i:i + chunk_size]
        process = multiprocessing.Process(target=summarize, args=(chunk, summ))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f'result is {summ.value}. Time elapsed: {time.time() - start_time:2f}')


if __name__ == '__main__':
    main()
