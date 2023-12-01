from http import HTTPStatus

from api.v1.queries.genre import query_genre
from api.v1.schemas.genre import GenreDetailSchema
from core.config import Settings
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import paginate
from services.collection import CollectionService, get_collection_service
from services.detail import DetailService, get_detail_service

from utils.pagination import Page

CONFIG = Settings()

router = APIRouter()


@router.get("/", response_model=Page[GenreDetailSchema])
async def genres_collection(
    genres_service: CollectionService = Depends(get_collection_service),
) -> dict:
    """Get genre collection with related films ordered by rating."""
    genres = await genres_service.get_item_collection(
        query_genre(),
        GenreDetailSchema,
        CONFIG.elastic.genre_idx
    )
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="genres not found")
    return paginate(genres)


@router.get("/{genre_id}", response_model=GenreDetailSchema)
async def genres_detail(
    genre_id: str, genres_service: DetailService = Depends(get_detail_service)
) -> GenreDetailSchema:
    """Get one genre with related films ordered by rating."""
    genre = await genres_service.get_item_by_id(GenreDetailSchema, CONFIG.elastic.genre_idx, genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="genre not found")
    return genre
