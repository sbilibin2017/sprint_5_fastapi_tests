from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import paginate

from api.v1.queries.search import query_film_by_title
from api.v1.schemas.search import SearchDetailSchema
from core.config import Settings
from services.search import SearchService, get_search_service
from utils.pagination import Page

CONFIG = Settings()

router = APIRouter()


@router.get("/", response_model=Page[SearchDetailSchema])
async def search_collection(
    title: str | None = Query(
        default='Star',
        description='Film title or its part'
    ),
    search_service: SearchService = Depends(get_search_service)
) -> dict:
    """Search films with title."""
    search = await search_service.get_item_collection(
        query_film_by_title(title),
        SearchDetailSchema,
        CONFIG.elastic.search_idx
    )
    if not search:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="film not found")
    return paginate(search)
