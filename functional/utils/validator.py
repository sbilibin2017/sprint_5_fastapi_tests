from datetime import date, datetime

from pydantic import BaseModel

from utils.mixin import FilmIDMixin, GenreMixin, PersonMixin


class PostgresPydantic(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: int


class ElasticPydantic(BaseModel):
    host: str
    port: int


class RedisPydantic(BaseModel):
    host: str
    port: int


class Film(BaseModel):
    id: FilmIDMixin
    title: str
    imdb_rating: float
    type: str
    description: str
    creation_date: date
    file_path: str
    created_at: datetime
    updated_at: datetime


class Film4Genre(GenreMixin):
    film_id: str
    genre_id: str
    created_at: datetime


class Film4Person(PersonMixin):
    film_id: str
    person_id: str
    role: str
    created_at: datetime


class FilmElastic(BaseModel):
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


class GenreElastic(GenreMixin):
    film: list[FilmIDMixin]


class PersonElastic(PersonMixin):
    film: list[FilmIDMixin]
