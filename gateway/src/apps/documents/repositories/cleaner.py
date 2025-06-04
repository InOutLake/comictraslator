from typing import Annotated, Protocol, Self
from fastapi import Depends
from gateway.src.apps.documents.enums import CleanerActions
from gateway.src.apps.documents.schemas.services.cleaner import CleanRequest
from shared.repositories.rmqrepository import RMQRPCClient
from shared.settings import settings


class CleanerRepository(Protocol):
    async def clean(self: Self, data: CleanRequest) -> str: ...


class CleanerRabbitMQRepository(CleanerRepository, RMQRPCClient):
    exchange_name = "Cleaner"

    async def clean(self: Self, data: CleanRequest) -> str:
        response = await self.do(CleanerActions.CLEAN, data)
        return response


async def ocr_repository_factory() -> CleanerRepository:
    repo = CleanerRabbitMQRepository(settings=settings)
    await repo.initialize()
    return repo


CleanerRepositoryDep = Annotated[CleanerRepository, Depends(ocr_repository_factory)]
