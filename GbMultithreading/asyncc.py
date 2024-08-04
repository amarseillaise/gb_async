import asyncio
import aiohttp
from pathlib import Path
import time


async def parser(url: str, session):
    async with session.get(url) as response:
        body = await response.text()
    Path('htmls').mkdir(exist_ok=True)
    filename = './htmls/' + url.replace('https://', '',).replace('.', '-') + '.html'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(body)


async def main():
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
    tasks = []

    time_start = time.time()
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(asyncio.create_task(parser(url, session)))
        await asyncio.gather(*tasks)
    time_finish = time.time() - time_start
    print(f'Time elapsed {time_finish:1f} seconds')


if __name__ == '__main__':
    asyncio.run(main())
