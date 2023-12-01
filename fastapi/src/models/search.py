import orjson
from pydantic import BaseModel

from utils.mixin import GenreMixin, PersonMixin
from utils.orjson import orjson_dumps


class Search(BaseModel):
    id: str
    title: str
    imdb_rating: float | None
    type: str | None
    creation_date: str | None
    description: str | None
    genre__name: list[str]
    director__full_name: list[str]
    writer__full_name: list[str]
    actor__full_name: list[str]
    genre: list[GenreMixin]
    director: list[PersonMixin]
    writer: list[PersonMixin]
    actor: list[PersonMixin]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps