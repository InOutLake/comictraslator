from typing import Annotated, Any, List, Protocol, Self

from fastapi import Depends
from gateway.src.apps.documents.enums import OCRActions
from gateway.src.common.repositories.rmqrepository import RMQRPCClient
from src.apps.documents.schemas.documents import Page
from src.apps.documents.schemas.ocr import FindAreasResponse, GetTextResponse
from src.common.settings import settings


class OCRRepository(Protocol):
    def find_areas(self: Self, pages: List[Page]): ...
    def get_text(self: Self, page_areas: Any): ...


class OCRRabbitMQRepository(OCRRepository, RMQRPCClient):
    exchange_name = "OCR"

    async def find_areas(self: Self, pages: List[Page]):
        response = await self.do(OCRActions.FIND_AREAS, pages)
        return FindAreasResponse.model_validate_json(response)

    async def get_text(self: Self, pages_areas: Any):
        response = await self.do(OCRActions.GET_TEXT, pages_areas)
        return GetTextResponse.model_validate_json(response)


def ocr_repository_factory() -> OCRRepository:
    repo = OCRRabbitMQRepository(settings=settings)
    return repo


OCRRepositoryDep = Annotated[OCRRepository, Depends(ocr_repository_factory)]
