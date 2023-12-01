from pydantic import BaseModel


class FilmIDMixin(BaseModel):
    id: str


class GenreMixin(BaseModel):
    id: str
    name: str


class PersonMixin(BaseModel):
    id: str
    full_name: str
