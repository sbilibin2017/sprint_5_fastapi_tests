from http import HTTPStatus

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from fastapi_pagination import paginate

from api.v1.queries.film import query_films, query_films_by_genre, query_films_by_genre_with_sort, query_films_with_sort
from api.v1.schemas.film import FilmDetailSchema
from core.config import Settings
from services.collection import CollectionService, get_collection_service
from services.detail import DetailService, get_detail_service
from utils.pagination import Page

CONFIG = Settings()


app = FastAPI()


router = APIRouter()


app = FastAPI()


@router.get("/", response_model=Page[FilmDetailSchema])
async def film_collection(
    films_service: CollectionService = Depends(get_collection_service),
    genre: str | None = Query(
        default=None,
        description='You can use only: \
            Action, Adventure, Animation, Biography, \
            Comedy, Crime, Documentary, Drama, Family, Fantasy'
    ),
    sort: str | None = Query(
        default='-imdb_rating',
        regex='^-?(imdb_rating|title)',
        description='You can use only: imdb_rating, -imdb_rating, title, -title'
    ),
) -> dict:
    """Get paginated film collection with genres filter and ordered by date."""
    if (genre is not None) & (sort is None):
        query = query_films_by_genre(genre.split(','))
    elif (genre is None) & (sort is None):
        query = query_films()
    elif (genre is None) & (sort is not None):
        query = query_films_with_sort(sort)
    elif (genre is not None) & (sort is not None):
        query = query_films_by_genre_with_sort(genre.split(','), sort)

    films = await films_service.get_item_collection(
        query,
        FilmDetailSchema,
        CONFIG.elastic.film_idx
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="films not found")

    return paginate(films)


@router.get("/{film_id}", response_model=FilmDetailSchema)
async def film_detail(film_id: str, film_service: DetailService = Depends(get_detail_service)) -> FilmDetailSchema:
    """Get one film with related films ordered by rating."""
    film = await film_service.get_item_by_id(FilmDetailSchema, CONFIG.elastic.film_idx, film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="film not found")
    return film
