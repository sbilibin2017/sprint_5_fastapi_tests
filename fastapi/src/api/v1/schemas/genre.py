from utils.mixin import FilmIDMixin, GenreMixin


class GenreDetailSchema(GenreMixin):
    film: list[FilmIDMixin]
