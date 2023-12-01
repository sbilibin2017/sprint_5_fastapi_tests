import orjson

from utils.mixin import FilmIDMixin, GenreMixin
from utils.orjson import orjson_dumps


class GenreElastic(GenreMixin):
    film: list[FilmIDMixin]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
