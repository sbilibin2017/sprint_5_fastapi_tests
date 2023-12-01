import orjson

from utils.mixin import FilmIDMixin, PersonMixin
from utils.orjson import orjson_dumps


class WriterElastic(PersonMixin):
    film: list[FilmIDMixin]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
