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
async def writer_collection(
    writers_service: CollectionService = Depends(get_collection_service),
) -> dict:
    """Get writers collection with related films ordered by rating."""
    writers = await writers_service.get_item_collection(
        query_person(),
        PersonDetailSchema,
        CONFIG.elastic.writer_idx
    )
    if not writers:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="writers not found")
    return paginate(writers)


@router.get("/{writer_id}", response_model=PersonDetailSchema)
async def actor_detail(
    writer_id: str, writer_service: DetailService = Depends(get_detail_service)
) -> PersonDetailSchema:
    """Get one writer with related films ordered by rating."""
    writer = await writer_service.get_item_by_id(PersonDetailSchema, CONFIG.elastic.writer_idx, writer_id)
    if not writer:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="writer not found")
    return writer
