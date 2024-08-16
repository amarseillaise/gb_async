import json
from json import JSONDecodeError
from pathlib import Path
import aiofiles

DB_FILE = 'movies.json'
DB_PATH = Path().absolute().joinpath(DB_FILE)
Path(DB_PATH).touch(exist_ok=True)

async def get_movies():
    try:
        async with aiofiles.open(DB_PATH, 'r') as f:
            content = await f.read()
        return json.loads(content)
    except JSONDecodeError:
        return {}

async def get_movie(movie_id):
    try:
        async with aiofiles.open(DB_PATH, 'r') as f:
            content = await f.read()
        movies_dict = json.loads(content)
        return movies_dict.get(str(movie_id), {})
    except JSONDecodeError:
        return {}

async def add_movie(movie):
    movies = await get_movies()
    movies[str(movie['id'])] = movie
    print(movies)
    async with aiofiles.open(DB_PATH, 'w') as f:
        await f.write(json.dumps(movies, indent=2))

# async def main():
#     re = await get_movie(4)
#     print(re)
#
# if __name__ == '__main__':
#     asyncio.run(main())