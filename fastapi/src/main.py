from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from redis.asyncio import Redis

from api.v1 import actors, directors, films, genres, search, writers
from core.config import Settings
from db import elastic, redis

CONFIG = Settings()
PROJECT_NAME = CONFIG.project.project_name

app = FastAPI(
    title=f"Read-only API for online cinema ({PROJECT_NAME}).",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis.redis = Redis(
        host=CONFIG.redis.host, port=CONFIG.redis.port, decode_responses=True)
    elastic.es = AsyncElasticsearch(hosts=[CONFIG.elastic.url])


@app.on_event("shutdown")
async def shutdown():
    redis.redis.close()
    elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(actors.router, prefix="/api/v1/actors", tags=["actors"])
app.include_router(writers.router, prefix="/api/v1/writers", tags=["writers"])
app.include_router(
    directors.router, prefix="/api/v1/directors", tags=["directors"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])

add_pagination(app)
