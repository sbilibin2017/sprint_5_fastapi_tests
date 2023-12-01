from http import HTTPStatus

from api.v1.queries.person import query_person
from api.v1.schemas.person import PersonDetailSchema
from core.config import Settings
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import paginate
from services.collection import CollectionService, get_collection_service
from services.detail import DetailService, get_detail_service

from utils.pagination import Page

CONFIG = Settings()

router = APIRouter()


@router.get("/", response_model=Page[PersonDetailSchema])
async def director_collection(
    directors_service: CollectionService = Depends(get_collection_service)
) -> dict:
    """Get directors collection with related films ordered by rating."""
    directors = await directors_service.get_item_collection(
        query_person(
        ), PersonDetailSchema, CONFIG.elastic.director_idx
    )
    if not directors:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="directors not found")
    return paginate(directors)


@router.get("/{director_id}", response_model=PersonDetailSchema)
async def director_detail(
    director_id: str, director_service: DetailService = Depends(get_detail_service)
) -> PersonDetailSchema:
    """Get one director with related films ordered by rating."""
    director = await director_service.get_item_by_id(
        PersonDetailSchema,
        CONFIG.elastic.director_idx,
        director_id
    )
    if not director:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="director not found")
    return director
