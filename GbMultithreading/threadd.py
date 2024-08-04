import threading
import requests
from pathlib import Path
import time


def parser(url: str):
    response = requests.get(url)
    Path('htmls').mkdir(exist_ok=True)
    filename = './htmls/' + url.replace('https://', '',).replace('.', '-') + '.html'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)


def main():
    urls = [
        'https://ya.ru',
        'https://google.com',
        'https://stackoverflow.com',
        'https://mail.ru',
        'https://vk.ru',
        'https://gb.ru',
        'https://www.youtube.com',
        'https://www.twitch.tv',
        'https://www.reddit.com',
    ]
    threads = []

    time_start = time.time()
    for url in urls:
        thread = threading.Thread(target=parser, args=[url])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    time_finish = time.time() - time_start
    print(f'Time elapsed {time_finish:1f} seconds')


if __name__ == '__main__':
    main()
