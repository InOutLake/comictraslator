from typing import Annotated, Any, Coroutine, List, Protocol, Self

from fastapi import Depends
from gateway.src.apps.documents.enums import OCRActions
from shared.repositories.rmqrepository import RMQRPCClient
from gateway.src.apps.documents.schemas.documents import Page
from gateway.src.apps.documents.schemas.ocr import FindAreasResponse, GetTextResponse
from gateway.src.common.settings import settings


class OCRRepository(Protocol):
    async def find_areas(self: Self, pages: Page) -> FindAreasResponse: ...

    async def get_text(self: Self, page_areas: Any) -> GetTextResponse: ...


class OCRRabbitMQRepository(OCRRepository, RMQRPCClient):
    exchange_name = "OCR"

    async def find_areas(self: Self, pages: Page) -> FindAreasResponse:
        response = await self.do(OCRActions.FIND_AREAS, pages)
        return FindAreasResponse.model_validate_json(response)

    async def get_text(self: Self, page_areas: Any):
        response = await self.do(OCRActions.GET_TEXT, page_areas)
        return GetTextResponse.model_validate_json(response)


def ocr_repository_factory() -> OCRRepository:
    repo = OCRRabbitMQRepository(settings=settings)
    return repo


OCRRepositoryDep = Annotated[OCRRepository, Depends(ocr_repository_factory)]
