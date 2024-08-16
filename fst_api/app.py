from http.client import HTTPException
from typing import List

from aiostream import stream

from fastapi import FastAPI, HTTPException
from fst_api.models import Movie
from fst_api.data_io import get_movies, get_movie, add_movie

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, GbFastApi!"}

@app.get("/movie/{movie_id}")
async def return_movie(movie_id: str):
    movie = await get_movie(movie_id)
    if movie:
        return Movie.model_construct(**movie)
    raise HTTPException(status_code=404, detail="Movie not found")

@app.get("/movies/", response_model=List[Movie])
async def return_all_movies():
    movies = await get_movies()
    movies = stream.iterate(list(movies.values()))
    if movies:
        result = []
        async for movie in movies:
            result.append(Movie.model_construct(**movie))
        return result
    raise HTTPException(status_code=404, detail="Movie not found")


@app.post("/movies/create/")
async def create_movie(movie_data: Movie):
    await add_movie(movie_data.model_dump())
    return {"message": "movie created"}

