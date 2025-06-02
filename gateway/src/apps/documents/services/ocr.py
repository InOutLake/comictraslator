from apps.documents.schemas.documents import Page
from apps.documents.schemas.ocr import FindAreasResponse, GetTextResponse
from fastapi import Depends
from gateway.src.apps.documents.repositories.ocr import (
    OCRRepository,
    OCRRepositoryDep,
)
from typing import Annotated, Any, Protocol, Self


class OCRService(Protocol):
    async def find_areas(self: Self, pages: Page) -> FindAreasResponse: ...

    async def get_text(self: Self, page_areas: Any) -> GetTextResponse: ...


class OCRServiceImpl(OCRService):
    def __init__(self: Self, ocr: OCRRepository):
        self.ocr = ocr

    async def find_areas(self: Self, pages: Page) -> FindAreasResponse:
        result = await self.ocr.find_areas(pages)
        return FindAreasResponse.model_validate(result)

    async def get_text(self: Self, page_areas: Page) -> GetTextResponse:
        result = await self.ocr.get_text(page_areas)
        return GetTextResponse.model_validate(result)


def ocr_service_factory(ocr: OCRRepositoryDep):
    return OCRServiceImpl(ocr=ocr)


OCRServiceDep = Annotated[OCRService, Depends(ocr_service_factory)]
