from typing import Annotated, Any, Protocol, Self
from fastapi import Depends
from gateway.src.apps.documents.enums import CleanerActions
from shared.repositories.rmqrepository import RMQRPCClient
from apps.documents.schemas.services.ocr import FindAreasResponse, GetTextResponse
from shared.settings import settings


class CleanerRepository(Protocol):
    async def clean(self: Self, page_url: str, fields: Any) -> str: ...


class CleanerRabbitMQRepository(CleanerRepository, RMQRPCClient):
    exchange_name = "Cleaner"

    async def clean(self: Self, data: CleanRequest) -> FindAreasResponse:
        response = await self.do(CleanerActions.CLEAN, data)
        return response.decode()


async def ocr_repository_factory() -> CleanerRepository:
    repo = CleanerRabbitMQRepository(settings=settings)
    await repo.initialize()
    return repo


CleanerRepositoryDep = Annotated[CleanerRepository, Depends(ocr_repository_factory)]
