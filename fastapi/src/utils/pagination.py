from __future__ import annotations

from typing import Generic, TypeVar

from fastapi import Query
from fastapi_pagination.default import Page as BasePage
from fastapi_pagination.default import Params as BaseParams

from core.config import Settings

settings = Settings()

T = TypeVar("T")


class Params(BaseParams):
    size: int = Query(settings.default_page_size,
                      ge=1, description='Page size.')
    page: int = Query(settings.default_page_number,
                      ge=1, description='Page number.')


class Page(BasePage[T], Generic[T]):
    __params_type__ = Params
