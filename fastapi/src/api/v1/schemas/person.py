from utils.mixin import FilmIDMixin, PersonMixin


class PersonDetailSchema(PersonMixin):
    film: list[FilmIDMixin]
