from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import paginate

from api.v1.queries.person import query_person
from api.v1.schemas.person import PersonDetailSchema
from core.config import Settings
from services.collection import CollectionService, get_collection_service
from services.detail import DetailService, get_detail_service
from utils.pagination import Page

CONFIG = Settings()

router = APIRouter()


@router.get("/", response_model=Page[PersonDetailSchema])
async def actor_collection(
    actors_service: CollectionService = Depends(get_collection_service),
) -> dict:
    """Get actors collection with related films ordered by rating."""
    actors = await actors_service.get_item_collection(
        query_person(
        ), PersonDetailSchema, CONFIG.elastic.actor_idx
    )
    if not actors:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="actors not found")
    return paginate(actors)


@router.get("/{actor_id}", response_model=PersonDetailSchema)
async def actor_detail(
    actor_id: str, actor_service: DetailService = Depends(get_detail_service)
) -> PersonDetailSchema:
    """Get one actor with related films ordered by rating."""
    actor = await actor_service.get_item_by_id(
        PersonDetailSchema,
        CONFIG.elastic.actor_idx,
        actor_id
    )
    if not actor:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="actor not found")
    return actor
